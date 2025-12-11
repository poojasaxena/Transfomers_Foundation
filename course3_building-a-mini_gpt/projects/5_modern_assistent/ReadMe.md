# Project 5: Tiny GPT with Byte-Level BPE (v3)

This project builds a **small, friendly GPT language model** using byte-level BPE tokenization.  
It is a continuation of Project-4 but with a **modern BPE tokenizer** and clean training / inference scripts.

---

## Folder Structure

5_tiny_gpt_bpe_v3/
├── config.json # Project configuration
├── ReadMe.md
├── train_bpe_gpt_v3.py # Training script
├── generate.py # Interactive text generation
└── resources/ # Optional datasets or reference files



---

## Setup

1. Ensure `llmlib` is installed and accessible in your Python environment.
2. Set global directories (optional):

```bash
export GLOBAL_DATASETS_DIR=~/Datasets
export GLOBAL_MODELS_DIR=~/Models
```
3.Place your dataset in $GLOBAL_DATASETS_DIR/llm/mixed_text/data.txt.
4. Make sure tokenizer exists at:
```
$GLOBAL_MODELS_DIR/llm/tokenizers/bpe-greet/v3/tokenizer.json
```