import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import torch.optim as optim

from pathlib import Path
import json
from llmlib.io import load_project_config, save_modern_gpt_model, get_data_file_path
from llmlib.modern_gpt import ModernGPTConfig, ModernGPTModel
from llmlib.modern_byte_bpe import ModernByteBPETokenizer

# ------------------------------
# Dataset
# ------------------------------

class TextDataset(Dataset):
    def __init__(self, file_path: Path, tokenizer: ModernByteBPETokenizer, block_size: int):
        with file_path.open("r", encoding="utf-8") as f:
            self.text = f.read()

        self.tokenizer = tokenizer
        self.block_size = block_size
        self.tokens = self.tokenizer.encode(self.text)

    def __len__(self):
        return max(1, len(self.tokens) - self.block_size)

    def __getitem__(self, idx):
        x = torch.tensor(self.tokens[idx: idx + self.block_size], dtype=torch.long)
        y = torch.tensor(self.tokens[idx + 1: idx + 1 + self.block_size], dtype=torch.long)
        return x, y

# ------------------------------
# Training
# ------------------------------

def main():
    # Load project config
    config = load_project_config(__file__)
    model_cfg = config["model_config"]
    training_cfg = config["training_config"]
    metadata = config["project_metadata"]

    # Tokenizer
    tok_path = metadata.get("tokenizer_save_path")
    tokenizer = ModernByteBPETokenizer.from_dict(json.load(open(tok_path, "r", encoding="utf-8")))

    # Dataset
    data_file = get_data_file_path(config)
    dataset = TextDataset(data_file, tokenizer, block_size=training_cfg["block_size"])
    dataloader = DataLoader(dataset, batch_size=training_cfg["batch_size"], shuffle=True)

    # Model
    mg_cfg = ModernGPTConfig(
        vocab_size=len(tokenizer.vocab),
        d_model=model_cfg.get("d_model", 256),
        n_heads=model_cfg.get("n_heads", 8),
        n_layers=model_cfg.get("n_layers", 8),
        max_position_embeddings=model_cfg.get("max_position_embeddings", 256),
        dropout=model_cfg.get("dropout", 0.1)
    )
    model = ModernGPTModel(mg_cfg)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    optimizer = optim.Adam(model.parameters(), lr=training_cfg["learning_rate"])
    criterion = nn.CrossEntropyLoss()

    # Training loop
    model.train()
    for epoch in range(training_cfg["num_epochs"]):
        for i, (x, y) in enumerate(dataloader):
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits.view(-1, logits.size(-1)), y.view(-1))
            loss.backward()
            optimizer.step()

            if (i + 1) % 50 == 0:
                print(f"Epoch {epoch+1}, step {i+1}, loss: {loss.item():.4f}")

    # Save model
    save_modern_gpt_model(model, config)
    print("Training finished and model saved!")

if __name__ == "__main__":
    main()
