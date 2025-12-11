# Tiny Transformer – Intro Project

This project demonstrates a minimal end-to-end workflow for training a **tiny GPT-style Transformer model** using the `llmlib` library.

It is intentionally small, simple, and easy to modify — perfect for understanding how a GPT-like model works under the hood.

---

## 📁 Project Structure

1_tiny_transformer_intro/
│
├── project_config.json # Experiment configuration (nested format)
├── train.py # Manual training script
├── run_inference.py # Manual inference script
└── ReadMe.md # This file


* All core model logic (tokenizer, model, config, save/load utilities, CLI tools) lives inside
  `$WORKBENCH_ROOT/Tools/Python/PLibraries/llmlib`


---

## ⚙️ Configuration (`project_config.json`)

This project uses a structured nested configuration format:

```json
{
  "model_config": {
    "d_model": 16,
    "n_heads": 2,
    "n_layers": 2,
    "max_position_embeddings": 32,
    "dropout": 0.1
  },
  "training_config": {
    "batch_size": 64,
    "learning_rate": 0.003,
    "train_steps": 1200,
    "num_epochs": 10,
    "eval_interval": 100,
    "eval_iters": 200
  },
  "project_metadata": {
    "model_name": "tiny-gpt-greet-v1",
    "model_save_path": "llm/TinyTransformer_Program",
    "data_path": "llm/greetings",
    "data_file": "greetings.txt",
    "max_seq_length": 32,
    "max_new_tokens": 20
  }
}
```
* The tokenizer vocabulary (`VOCAB_SIZE`) is automatically included in the saved `tiny_config.json` along with the trained model.

## 🚀 Training the Model (recommended via CLI)
Once `llmlib` is installed in editable mode:

```
pip install -e ~/PoojaVault/Professional/Workbench/Tools/Python/PLibraries/llmlib
```
Follow one of the two approaches:

### 1. Script approach
```
python course3_building-a-mini_gpt/projects/1_tiny_transformer_intro/train.py
```


### 2. CLI approach
```
tiny-gpt-train \
  --config "$LEARNING_ROOT/NLP_and_LLMs/Transformers_Fundamentals/course3_building-a-mini_gpt/projects/1_tiny_transformer_intro/project_config.json" \
  --device auto
```
This will:
* load tokenizer + dataset
* build a TinyTransformer
*train for train_steps
* save: 
    ```
    $GLOBAL_MODELS_DIR/llm/TinyTransformer_Program/tiny-gpt-greet-v1/
    ├── model.pt
    └── tiny_config.json
    ```

## 💬 Generating Text

### 1. Script approach
```
## Inference
python course3_building-a-mini_gpt/projects/1_tiny_transformer_intro/run_inference.py
```

### 2. ClI approach
* one shot prompt
    ```
    tiny-gpt-infer \
    --config "$LEARNING_ROOT/NLP_and_LLMs/Transformers_Fundamentals/course3_building-a-mini_gpt/projects/1_tiny_transformer_intro/project_config.json" \
    --prompt "hello"
    ```

* Interactive mode
    ```
    tiny-gpt-infer \
  --config "$LEARNING_ROOT/NLP_and_LLMs/Transformers_Fundamentals/course3_building-a-mini_gpt/projects/1_tiny_transformer_intro/project_config.json"
    ```

## 📦 Saved Model Format
```
tiny-gpt-greet-v1/
├── model.pt             # Model weights
└── tiny_config.json     # Full reproducible config (model + training + metadata)
```
> This `tiny_config.json` file contains everything required to reproduce the run.