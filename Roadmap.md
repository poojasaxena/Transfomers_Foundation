# MASTER ROADMAP — Your Practical LLM Program

## PHASE 1 — PyTorch for LLMs (5 days)

Build exact foundations needed for attention + transformer internals.

Day 1 — Tensors, Shapes, Broadcasting, Causal Masks

1D, 2D, 3D tensor shapes

batch × seq × embed convention

causal masks (triangular)

padding masks

small hands-on exercises
✔️ Output: ability to reason about attention shapes

Day 2 — Implement Single-Head Attention (from scratch)

build Q, K, V

dot-product attention

softmax scaling

small forward pass
✔️ Output: minimal working attention function

Day 3 — Multi-Head Attention

split heads

concat back

projection matrices
✔️ Output: real multi-head attention layer like in GPT

Day 4 — Transformer Block

residual connections

layernorm

feed-forward network
✔️ Output: one working transformer block you coded yourself

Day 5 — Write a Mini Generation Loop

autoregressive generation

feeding the next token

controlling sequence length
✔️ Output: simplest possible GPT-like inference code


### Next Steps:

1. Add a CLI command (tiny-gpt-train / tiny-gpt-infer)

Just a thin wrapper so you can do:

tiny-gpt-train --config project_config.json
tiny-gpt-infer --model tiny-gpt-greet-v1

2. Swap character tokenizer → word tokenizer

This would be a one-file change in tokenizer.py.

3. Add attention masking in model (causal mask)

So the model cannot attend to future tokens — becomes more GPT-like.

4. Add a mini dataset loader class

Instead of putting batching logic inside train.py.


## PHASE 2 — HuggingFace + LLM Mechanics (7 days)

Move from tiny toy models → real LLM models.

Day 6 — Tokenizers: BPE, SP, WordPiece
Day 7 — Loading HF models manually
Day 8 — Sampling: temperature, top-k, top-p
Day 9 — KV Cache (why speed improves drastically)
Day 10 — Quantization: 8-bit, 4-bit, gguf
Day 11 — Family Tour: LLaMA, Mistral, Phi, Qwen
Day 12 — Evaluate a model locally

## PHASE 3 — Build Your First Real RAG App (5 days)

You will create your own small ChatGPT-like assistant.

Day 13 — Embeddings models
Day 14 — Vector stores: FAISS/Chroma
Day 15 — Retrieval pipeline
Day 16 — Building a combined RAG function
Day 17 — Evaluation + debugging hallucinations
PHASE 4 — Fine-Tuning / LoRA (7 days)

Train your own small LLM on a tiny dataset.

Day 18 — What is LoRA / QLoRA?
Day 19 — Dataset preparation
Day 20 — Training config
Day 21 — Training run
Day 22 — Inference with LoRA weights
Day 23 — Evaluating model improvements
Day 24 — How to deploy / reuse your fine-tuned model