## How to run pipeline
```
# Validate first (Dry Run)
llmlib train-pipeline --config config.json --dry-run

# TMux Dry Run
llmlib tmux start --config config.json --dry-run

# Unified CLI Dry Run
llmlib train-pipeline --config config.json --dry-run  # Same as #1

# Step 1: Quick validation (interactive, immediate feedback)
llmlib train-pipeline --config config.json --dry-run

# Step 2: If validation passes, start long training in tmux
llmlib tmux start --config config.json --auto-confirm

# Monitor progress (separate terminal)
llmlib tmux monitor

# Attach when needed
llmlib tmux attach session-name
```

### Detailed Steps
1. Validate
```
llmlib train-pipeline --config 5_complex_architecture/config.json --dry-run
2025-12-18 13:50:55,675 | INFO | llmlib.cli.train_pipeline_cli | ✅ Config loaded: /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/5_complex_architecture/config.json
2025-12-18 13:50:55,676 | INFO | llmlib.cli.train_pipeline_cli | 🤖 Starting Robust LLM Training Pipeline
2025-12-18 13:50:55,676 | INFO | llmlib.cli.train_pipeline_cli | 📅 Started at: 2025-12-18 13:50:55.676152
2025-12-18 13:50:55,676 | INFO | llmlib.cli.train_pipeline_cli | 🖥️  Host: pooja-saxena-ThinkPad-L13-Yoga-Gen-4
2025-12-18 13:50:55,676 | INFO | llmlib.cli.train_pipeline_cli | 💾 Available space: 157.0 GB
2025-12-18 13:50:55,676 | INFO | llmlib.cli.train_pipeline_cli | 🔧 GLOBAL_DATASETS_DIR: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets
2025-12-18 13:50:55,676 | INFO | llmlib.cli.train_pipeline_cli | 🔧 GLOBAL_MODELS_DIR: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models
2025-12-18 13:50:55,677 | WARNING | llmlib.cli.train_pipeline_cli | ⚠️  nvidia-smi not available
2025-12-18 13:50:55,677 | INFO | llmlib.cli.train_pipeline_cli | 🔍 === DRY RUN: Validating all paths and dependencies ===
2025-12-18 13:50:55,677 | INFO | llmlib.cli.train_pipeline_cli | ✅ Config file: /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/5_complex_architecture/config.json
2025-12-18 13:50:55,677 | INFO | llmlib.cli.train_pipeline_cli | ✅ Tokenizer EXISTS: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/tokenizers/bpe-elephant/v4/tokenizer.json
2025-12-18 13:50:55,677 | INFO | llmlib.cli.train_pipeline_cli | 📁 Model directory EXISTS: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt
2025-12-18 13:50:55,683 | INFO | llmlib.cli.train_pipeline_cli | ✅ Training data EXISTS: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/train.txt (10,844 lines)
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli | ✅ Validation data EXISTS: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/val.txt (1,355 lines)
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli | 
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli | 🎯 Execution Plan:
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli |    1️⃣ Skip tokenizer training (already exists)
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli |    2️⃣ Train model → /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli |    3️⃣ Test inference with sample prompt
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli | 
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli | ⏱️  Estimated time: 4-6 hours for model training
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli | 🔄 Max retries: 3
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli | ⏰ Timeout: 8 hours
2025-12-18 13:50:55,684 | INFO | llmlib.cli.train_pipeline_cli | 
2025-12-18 13:50:55,685 | INFO | llmlib.cli.train_pipeline_cli | 🔍 Dry run completed - all checks passed!

```

2. Start TMux Training
```
llmlib tmux start --config 5_complex_architecture/config.json --auto-confirm
2025-12-18 13:52:13,939 | INFO | llmlib.cli.tmux_cli | 🚀 Starting training session: llmlib-config-1218_1352
2025-12-18 13:52:13,967 | INFO | llmlib.cli.tmux_cli | ✅ Created tmux session: llmlib-config-1218_1352
2025-12-18 13:52:13,967 | INFO | llmlib.cli.tmux_cli | ✅ Training started in session: llmlib-config-1218_1352
2025-12-18 13:52:13,967 | INFO | llmlib.cli.tmux_cli | 📺 To attach: tmux attach-session -t llmlib-config-1218_1352
2025-12-18 13:52:13,967 | INFO | llmlib.cli.tmux_cli | 📺 Or use: llmlib tmux attach llmlib-config-1218_1352
2025-12-18 13:52:13,967 | INFO | llmlib.cli.tmux_cli | 🔍 To monitor: llmlib tmux status
```