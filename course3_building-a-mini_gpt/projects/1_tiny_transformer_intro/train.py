import torch # type: ignore
import torch.nn as nn
import torch.optim as optim

from llmlib.tiny_config import TinyConfig
from llmlib.tiny_model import TinyTransformerModel
from llmlib.io import load_project_config, get_data_file_path, save_tiny_model
from llmlib.tokenizer import encode, decode, VOCAB_SIZE

# ---------------------------------------------------------
# 1. Global model path configuration
# ---------------------------------------------------------
PROJECT_CONFIG = load_project_config(__file__, "project_config.json")

MODEL_CFG = PROJECT_CONFIG["model_config"]
TRAIN_CFG = PROJECT_CONFIG["training_config"]
META_CFG = PROJECT_CONFIG["project_metadata"]

MODEL_NAME = META_CFG["model_name"]
MAX_SEQ_LEN = META_CFG["max_seq_length"]

D_MODEL = MODEL_CFG["d_model"]
N_HEADS = MODEL_CFG["n_heads"]
N_LAYERS = MODEL_CFG["n_layers"]
DROPOUT = MODEL_CFG["dropout"]

BATCH_SIZE = TRAIN_CFG["batch_size"]
LR = TRAIN_CFG["learning_rate"]
TRAIN_STEPS = TRAIN_CFG["train_steps"]


# ---------------------------------------------------------
# 2. Tiny toy dataset
# ---------------------------------------------------------
corpus_path = get_data_file_path(PROJECT_CONFIG)
with open(corpus_path, "r", encoding="utf-8") as f:
    text = f.read()
encoded_data = [encode(t) for t in text.splitlines() if t]


# ---------------------------------------------------------
# 3. Dataloader-like batching
# ---------------------------------------------------------
def make_batch(batch_size:int):

    # pick random sequences
    batch = [ encoded_data[i] for i in torch.randint(0, len(encoded_data), (batch_size,))]
    
    # truncate each sequence to at most max_seq_len
    batch = [x[:MAX_SEQ_LEN] for x in batch]

    # pad to equal length
    max_len = max(len(x) for x in batch)
    padded = [torch.cat([x, torch.zeros(max_len - len(x), dtype=torch.long)]) for x in batch]

    batch = torch.stack(padded)  # (batch, seq_len)
    return batch


# ---------------------------------------------------------
# 4. Create model
# ---------------------------------------------------------
config = TinyConfig(
    vocab_size = VOCAB_SIZE,
    d_model    = D_MODEL,
    n_heads    = N_HEADS,
    n_layers   = N_LAYERS,
    max_position_embeddings = MAX_SEQ_LEN,
    dropout    = DROPOUT,
)

print("\n" + "=" * 60)
print("🚀 TinyTransformer Training Run")
print("=" * 60)
print(f"Model Name              : {MODEL_NAME}")
print(f"Vocabulary Size         : {config.vocab_size}")
print(f"d_model                 : {config.d_model}")
print(f"n_heads                 : {config.n_heads}")
print(f"n_layers                : {config.n_layers}")
print(f"dropout                 : {config.dropout}")
print(f"max_seq_length          : {config.max_position_embeddings}")
print(f"batch_size              : {BATCH_SIZE}")
print(f"learning_rate           : {LR}")
print(f"train_steps             : {TRAIN_STEPS}")
print("=" * 60 + "\n")


model = TinyTransformerModel(config)
optimizer = optim.AdamW(model.parameters(), lr=LR)
criterion = nn.CrossEntropyLoss()


# ---------------------------------------------------------
# 5. Training loop (very small)
# ---------------------------------------------------------
for step in range(TRAIN_STEPS):
    input_ids = make_batch(BATCH_SIZE)

    ## Target = next token (shifted by 1)
    targets = input_ids[:, 1:].contiguous()
    inputs = input_ids[:, :-1].contiguous()

    ## Forward pass
    logits = model(inputs)  # (batch, seq_len-1, vocab_size)

    # reshape for loss: CE expects (batch*seq, vocab)
    loss = criterion(logits.view(-1, config.vocab_size), targets.view(-1))

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step % 10 == 0:
        print(f"Step {step}, Loss: {loss.item():.4f}")

# ---------------------------------------------------------
# 5b. Quick debug: inspect shapes on one example
# ---------------------------------------------------------
with torch.no_grad():
    example_text = "hello."
    example_ids = encode(example_text)[:MAX_SEQ_LEN]
    example_ids = example_ids.unsqueeze(0)  # (1, seq_len)

    logits = model(example_ids)
    print("\n[DEBUG] example_ids shape:", example_ids.shape)
    print("[DEBUG] logits shape      :", logits.shape)


# ---------------------------------------------------------
# 6. Save model + config (GLOBAL DIRECTORY)
# ---------------------------------------------------------
save_tiny_model(model, PROJECT_CONFIG)
