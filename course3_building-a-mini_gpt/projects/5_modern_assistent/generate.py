import torch
import json
from llmlib.io import load_project_config, load_modern_gpt_model, load_tokenizer_path
from llmlib.modern_byte_bpe import ModernByteBPETokenizer

# ------------------------------
# Text generation
# ------------------------------


def generate_text(
    model,
    tokenizer: ModernByteBPETokenizer,
    prompt: str,
    max_new_tokens: int = 50,
    device: str = "cpu",
):
    model.eval()
    input_ids = torch.tensor([tokenizer.encode(prompt)], dtype=torch.long).to(device)

    for _ in range(max_new_tokens):
        logits = model(input_ids)
        next_token_logits = logits[:, -1, :]
        probs = torch.softmax(next_token_logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1)
        input_ids = torch.cat([input_ids, next_id], dim=1)

    output_ids = input_ids[0].tolist()
    text = tokenizer.decode(output_ids)
    return text


# ------------------------------
# Main
# ------------------------------


def main():
    config = load_project_config(__file__)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load tokenizer
    tok_path = load_tokenizer_path(config)
    with tok_path.open("r", encoding="utf-8") as f:
        tokenizer = ModernByteBPETokenizer.from_dict(json.load(f))

    # Load model
    model = load_modern_gpt_model(config, device=device, eval_mode=True)

    while True:
        prompt = input("\nUser: ")
        if prompt.lower() in ["exit", "quit"]:
            break
        output = generate_text(
            model,
            tokenizer,
            prompt,
            max_new_tokens=config["project_metadata"].get("max_new_tokens", 80),
            device=device,
        )
        print(f"Assistant: {output}")


if __name__ == "__main__":
    main()
