#!/usr/bin/env python
import torch
from llmlib.io import load_tiny_model, load_project_config
from llmlib.tokenizer import encode, decode, VOCAB_SIZE

# from tiny_transformer_lab.tokenizer import TinyTokenizer  # if you have one

# ---------------------------------------------------------
# Project Config
# ---------------------------------------------------------
PROJECT_CONFIG = load_project_config(__file__, "project_config.json")
META_CFG = PROJECT_CONFIG["project_metadata"]

MODEL_NAME = META_CFG["model_name"]
MAX_SEQ_LEN = META_CFG["max_seq_length"]
MAX_NEW_TOKENS = META_CFG.get("max_new_tokens", 40)


# ---------------------------------------------------------
# Simple greedy generation
# ---------------------------------------------------------
def generate_text(model, prompt: str, max_new_tokens: int = MAX_NEW_TOKENS) -> str:
    model.eval()
    device = next(model.parameters()).device

    input_ids = encode(prompt)
    if input_ids.numel() == 0:
        return ""

    input_ids = input_ids.to(device)
    generated = input_ids.clone()

    temperature = 0.8  # < 1.0 = sharper, > 1.0 = more random

    for _ in range(max_new_tokens):
        context = generated[-MAX_SEQ_LEN:].unsqueeze(0)  # (1, seq_len)

        # torch.no_grad() for inference, very fast, no gradients needed, low memory
        with torch.no_grad():
            logits = model(context)        # (1, seq_len, vocab_size)
            next_logits = logits[0, -1, :] # (vocab_size,)
            probs = torch.softmax(next_logits, dim=-1) # now, every token has a probability

            # You can keep sampling or argmax here
            next_id = torch.multinomial(probs, num_samples=1).item()
            # or: next_id = torch.argmax(probs).item()

        generated = torch.cat([generated, torch.tensor([next_id], device=device)])

        # NEW: stop if we hit a period '.'
        next_char = decode(torch.tensor([next_id]))
        if next_char in [".", "?", "!"]:
            break

    return decode(generated.cpu())


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_tiny_model(PROJECT_CONFIG, device=device, eval_mode=True)

    print("\n============================================================")
    print("🧪 TinyTransformer Inference")
    print("============================================================")
    print(f"Model Name       : {MODEL_NAME}")
    print(f"Max Seq Length   : {MAX_SEQ_LEN}")
    print(f"Max New Tokens   : {MAX_NEW_TOKENS}")
    print(f"Device           : {device}")
    print("============================================================\n")

    prompt = input("Enter a prompt (e.g. 'hello'): ").strip()
    if not prompt:
        prompt = "hello."

    output = generate_text(model, prompt, max_new_tokens=40)

    print("\n---")
    print(f"Prompt : {prompt}")
    print(f"Output : {output}")


if __name__ == "__main__":
    main()
