from __future__ import annotations
import torch
import torch.nn.functional as F

from llmlib.io import load_project_config, load_tokenizer
from llmlib.io import load_modern_gpt_model as load_model


def top_k_filter(logits, top_k):
    """Keep only top-k tokens, set others to -inf."""
    if top_k is None or top_k <= 0:
        return logits
    values, indices = torch.topk(logits, top_k)
    min_values = values[:, -1].unsqueeze(-1)
    return torch.where(
        logits < min_values, torch.full_like(logits, -float("inf")), logits
    )


def top_p_filter(logits, top_p):
    """Nucleus sampling (top-p)."""
    if top_p is None or top_p >= 1.0:
        return logits

    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
    cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

    mask = cumulative_probs > top_p
    mask[:, 1:] = mask[:, :-1].clone()
    mask[:, 0] = False

    sorted_logits[mask] = -float("inf")

    logits_filtered = torch.full_like(logits, -float("inf"))
    logits_filtered.scatter_(1, sorted_indices, sorted_logits)
    return logits_filtered


def sample_next_token(
    logits,
    temperature=1.0,
    top_k=None,
    top_p=None,
    repetition_penalty=1.0,
    recent_tokens=None,
):
    """
    logits: tensor shape (1, V) for the last token (we assume batch=1).
    recent_tokens: iterable of token ids (list/set/tuple) to penalize.
    """
    # work on a copy
    logits = logits.clone()

    # repetition penalty (apply per-token, not set-indexing with a set)
    if recent_tokens is not None and repetition_penalty != 1.0:
        # convert to list of ints
        recent_tokens_list = list(recent_tokens)
        # safe in-place adjustment for the selected indices
        if len(recent_tokens_list) > 0:
            logits[0, recent_tokens_list] = (
                logits[0, recent_tokens_list] / repetition_penalty
            )

    # temperature
    if temperature != 1.0:
        logits = logits / temperature

    # top-k
    logits = top_k_filter(logits, top_k)

    # top-p
    logits = top_p_filter(logits, top_p)

    # convert to probs and sample
    probs = F.softmax(logits, dim=-1)
    next_id = torch.multinomial(probs, num_samples=1)  # shape (1,1)
    return int(next_id.item())


def generate(
    model,
    tokenizer,
    prompt,
    max_new_tokens=50,
    temperature=0.8,
    top_k=20,
    top_p=0.95,
    repetition_penalty=1.2,
    min_new_tokens=3,
    repetition_window=64,
):
    """
    Improved generation loop:
      - batch=1 incremental generation
      - per-token repetition penalty
      - stop on EOS after a minimum length
      - basic 'stall' detection (if last N tokens identical)
    """
    model.eval()
    device = next(model.parameters()).device

    # include special tokens in encoder if tokenizer supports them
    ids = tokenizer.encode(prompt, add_special_tokens=True)
    ids = torch.tensor(ids, dtype=torch.long, device=device).unsqueeze(0)  # (1, T)

    generated = ids[0].tolist()  # keep flat list for repetition checks
    recent_tokens = list(generated[-repetition_window:])

    for step in range(max_new_tokens):
        with torch.no_grad():
            logits = model(ids)  # (1, T, V)
            logits = logits[:, -1:, :].squeeze(1)  # (1, V) last token logits

            next_id = sample_next_token(
                logits,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                recent_tokens=recent_tokens,
            )

        # append token
        generated.append(next_id)
        # update ids tensor (append)
        ids = torch.cat(
            [ids, torch.tensor([[next_id]], dtype=torch.long, device=device)], dim=1
        )

        # update recent tokens window
        recent_tokens = list(generated[-repetition_window:])

        # stop if EOS and we've produced at least min_new_tokens
        tok_str = tokenizer.id_to_token.get(next_id, None)
        if min_new_tokens is not None and step + 1 < min_new_tokens:
            # do not allow early EOS
            pass
        else:
            if tok_str is not None and tok_str == tokenizer.config.eos_token:
                break

        # simple stall detection: if last 12 tokens are identical, break
        if len(generated) >= 12 and len(set(generated[-12:])) == 1:
            break

    # decode skipping special tokens
    return tokenizer.decode(generated, skip_special_tokens=True)


def main():
    cfg = load_project_config(__file__, "config.json")
    tokenizer = load_tokenizer(cfg)
    model = load_model(cfg, eval_mode=True)

    print("Model loaded. Ready.")

    while True:
        prompt = input("\nEnter prompt: ")
        out = generate(
            model,
            tokenizer,
            prompt,
            max_new_tokens=80,
            temperature=0.5,
            top_k=12,
            top_p=0.9,
            repetition_penalty=1.1,
        )
        print("\nGenerated:", out)


if __name__ == "__main__":
    main()
