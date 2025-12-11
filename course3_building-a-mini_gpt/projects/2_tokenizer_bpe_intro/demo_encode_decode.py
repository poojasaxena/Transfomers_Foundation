from __future__ import annotations

import sys

from llmlib import BPETokenizer
from llmlib.io import load_project_config, load_tokenizer_path
from llmlib.io import load_project_config, load_tokenizer


# ---------------------------------------------------------
# 1. Load project config + tokenizer
cfg = load_project_config(__file__, "project_config.json")
tokenizer = load_tokenizer(cfg)

text = "hola mundo esto es BPE"
ids = tokenizer.encode(text)
print("IDs:", ids)
print("Decoded:", tokenizer.decode(ids))

# ---------------------------------------------------------
# 2. Manual encode/decode example
def decode_encode_manually():
    cfg = load_project_config(__file__, "project_config.json")
    tok_path = load_tokenizer_path(cfg)

    if not tok_path.exists():
        raise SystemExit(
            f"Tokenizer not found at: {tok_path}\n"
            "Run `python train_tokenizer.py` first."
        )

    tokenizer = BPETokenizer.load(tok_path)

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text: ")

    ids = tokenizer.encode(text)
    print("Token IDs:", ids)
    print("Decoded:", tokenizer.decode(ids))
