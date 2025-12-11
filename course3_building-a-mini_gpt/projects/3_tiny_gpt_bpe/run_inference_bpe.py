from __future__ import annotations

import torch

from llmlib.io import load_project_config, load_tiny_model, load_tokenizer


def main():
    cfg = load_project_config(__file__, "config.json")

    tokenizer = load_tokenizer(cfg)
    model = load_tiny_model(cfg, eval_mode=True)

    if model.config.vocab_size != len(tokenizer.vocab):
        raise ValueError(
            f"Tokenizer vocab ({len(tokenizer.vocab)}) does not match model vocab ({model.config.vocab_size})."
        )


    prompt = input("Enter prompt: ")
    ids = tokenizer.encode(prompt)

    ids = torch.tensor(ids, dtype=torch.long)[None, :]  # batch=1

    for _ in range(cfg["project_metadata"]["max_new_tokens"]):
        logits = model(ids)
        next_id = torch.argmax(logits[:, -1, :], dim=-1)
        ids = torch.cat([ids, next_id[:, None]], dim=1)

    out = tokenizer.decode(ids[0].tolist())
    print("\nGenerated:", out)


if __name__ == "__main__":
    main()
