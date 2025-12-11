from __future__ import annotations

import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
import torch.optim as optim

from llmlib.io import (
    load_project_config,
    get_data_file_path,
    load_tokenizer,
    save_modern_gpt_model,
    get_model_paths,
)
from llmlib.modern_gpt import ModernGPTConfig, ModernGPTModel


class BPEDataset(Dataset):
    def __init__(self, texts, tokenizer, max_len):
        self.tokenizer = tokenizer
        self.max_len = max_len

        self.samples = []
        for line in texts:
            ids = tokenizer.encode(line)
            if len(ids) >= max_len:
                ids = ids[:max_len]
            self.samples.append(torch.tensor(ids, dtype=torch.long))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        x = self.samples[idx]
        return x[:-1], x[1:]


def collate_batch(batch):
    xs, ys = zip(*batch)
    max_len = max(x.size(0) for x in xs)

    padded_x, padded_y = [], []
    for x, y in zip(xs, ys):
        pad_len = max_len - x.size(0)
        padded_x.append(torch.cat([x, torch.full((pad_len,), 0)]))
        padded_y.append(torch.cat([y, torch.full((pad_len,), 0)]))

    return torch.stack(padded_x), torch.stack(padded_y)


def main():
    cfg = load_project_config(__file__, "config.json")
    train_cfg = cfg["training_config"]
    meta = cfg["project_metadata"]
    model_cfg = cfg["model_config"]

    tokenizer = load_tokenizer(cfg)
    vocab_size = len(tokenizer.vocab)

    data_path = get_data_file_path(cfg)
    with data_path.open() as f:
        lines = [l.strip() for l in f if l.strip()]

    max_len = meta["max_seq_length"]
    dataset = BPEDataset(lines, tokenizer, max_len)
    loader = DataLoader(
        dataset,
        batch_size=train_cfg["batch_size"],
        shuffle=True,
        collate_fn=collate_batch,
    )

    mg_cfg = ModernGPTConfig(
        vocab_size=vocab_size,
        d_model=model_cfg["d_model"],
        n_heads=model_cfg["n_heads"],
        n_layers=model_cfg["n_layers"],
        max_position_embeddings=model_cfg["max_position_embeddings"],
        dropout=model_cfg["dropout"],
    )
    model = ModernGPTModel(mg_cfg)

    optimizer = optim.AdamW(model.parameters(), lr=train_cfg["learning_rate"])
    steps = train_cfg["train_steps"]
    eval_interval = train_cfg["eval_interval"]

    model.train()
    step = 0

    while step < steps:
        for xb, yb in loader:
            logits = model(xb)
            loss = F.cross_entropy(logits.reshape(-1, vocab_size), yb.reshape(-1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if step % eval_interval == 0:
                print(f"Step {step}: loss = {loss.item():.4f}")

            step += 1
            if step >= steps:
                break

    save_modern_gpt_model(model, cfg)

    model_dir, ckpt_path, _ = get_model_paths(cfg)
    print("\n========= TRAINING COMPLETE (v2) =========")
    print(f"Model Name:            {meta['model_name']}")
    print(f"Model Directory:       {model_dir}")
    print(f"Checkpoint Saved At:   {ckpt_path}")
    print(f"Tokenizer Path:        {meta['tokenizer_save_path']}")
    print(f"Tokenizer Vocab Size:  {vocab_size}")
    print(f"Dataset File:          {data_path}")
    print(f"Total Samples:         {len(lines)}")
    print(f"Max Sequence Length:   {max_len}")
    print("=========================================\n")


if __name__ == "__main__":
    main()
