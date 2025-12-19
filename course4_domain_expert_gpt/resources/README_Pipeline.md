# 🚀 LLM Training Pipeline with Logging

Complete guide for training your elephant domain GPT model with robust logging, monitoring, and error recovery.

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `run_training_pipeline.sh` | Main training script with built-in logging |
| `start_training_with_logs.sh` | Easy one-command startup helper |
| `monitor_training.sh` | Monitor training progress without interrupting |
| `config_low_memory.json` | Memory-optimized config (prevents OOM kills) |
| `training_log_*.txt` | Automatically generated log files |

## 🎯 Quick Start (Recommended)

### Step 1: Navigate to Project Directory
```bash
cd "$LEARNING_ROOT/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects"
```

### Step 2A: Dry Run (Recommended First)
```bash
./start_training_with_logs.sh --dry-run
```
This will:
- ✅ Validate all paths and files
- ✅ Check tokenizer and data availability  
- ✅ Show exactly what will happen during training
- ✅ No actual training (safe to run anytime)

### Step 2B: Start Training with Automatic Logging
```bash
./start_training_with_logs.sh
```

This will:
- ✅ Create a timestamped log file (`training_log_YYYYMMDD_HHMMSS.txt`)
- ✅ Start training in a detached tmux session
- ✅ Show you monitoring commands
- ✅ Allow you to safely close your laptop

## 📊 Monitoring Your Training

### Option 1: Quick Status Check
```bash
./monitor_training.sh
```
Shows:
- Latest log file location
- Active tmux sessions
- Last 20 lines of output
- Training status (in progress/completed/failed)
- Error count

### Option 2: Watch Live Progress
```bash
tail -f training_log_*.txt
```
Real-time streaming of training output.

### Option 3: Filter Important Events
```bash
grep -E "(✅|❌|🔄|Step|Training attempt)" training_log_*.txt
```
Shows only key milestones and status updates.

### Option 4: Attach to Live Session
```bash
# Find your session name
tmux list-sessions

# Attach to it (replace SESSION_NAME with actual name)
tmux attach-session -t SESSION_NAME
```

## 🛠️ Alternative Startup Methods

### Method 1: Manual Tmux with Logging
```bash
LOG_FILE="training_log_$(date +%Y%m%d_%H%M%S).txt"
tmux new-session -d -s v4_training "script -f -q '$LOG_FILE' ./run_training_pipeline.sh"
```

### Method 2: Direct Script Execution
```bash
./run_training_pipeline.sh            # Full training
./run_training_pipeline.sh --dry-run  # Validation only
```
Note: This runs in current terminal (blocks) but still creates log files.

### Method 3: Background with nohup
```bash
nohup ./run_training_pipeline.sh > training_log_$(date +%Y%m%d_%H%M%S).txt 2>&1 &
```

## 📋 Useful Commands During Training

### Check System Resources
```bash
free -h                    # Memory usage
htop                       # CPU/Memory monitor
df -h                      # Disk space
ps aux | grep modern-gpt   # Find training process
```

### Tmux Session Management
```bash
tmux list-sessions                # List all sessions
tmux attach-session -t NAME       # Attach to session
tmux detach                       # Detach (Ctrl+B, then D)
tmux kill-session -t NAME         # Stop training session
```

### Log Analysis
```bash
# View entire log
less training_log_*.txt

# Search for specific terms
grep -i "error" training_log_*.txt
grep -i "epoch" training_log_*.txt
grep -i "loss" training_log_*.txt

# Count occurrences
grep -c "Training attempt" training_log_*.txt
grep -c "✅" training_log_*.txt

# Get training timing
grep "Started at\|completed at" training_log_*.txt
```

## ⚠️ Troubleshooting

### If Training Fails with OOM (Out of Memory)
The script uses `config_low_memory.json` with optimized settings:
- Batch size: 4 (instead of 16)
- Model dimensions: 256 (instead of 320)  
- Sequence length: 256 (instead of 384)
- Layers: 6 (instead of 8)

### If Tmux Session Dies
Check system logs for crashes:
```bash
journalctl --since "1 hour ago" | grep -E "(killed|crash|OOM)"
```

### If Training Stalls
The script has built-in auto-retry (3 attempts) and 8-hour timeout.

### Emergency Stop
```bash
# Find and kill training process
ps aux | grep modern-gpt
sudo kill -9 PID

# Or kill entire tmux session
tmux kill-session -t SESSION_NAME
```

## 📈 Expected Timeline

| Phase | Duration | Memory Usage |
|-------|----------|--------------|
| Tokenizer check | 1-2 min | ~1GB |
| Model training | 4-6 hours | ~4-6GB |
| Inference test | 1-2 min | ~2GB |
| **Total** | **~4-7 hours** | **Peak 6GB** |

## 🎉 Training Complete

When training finishes successfully, you'll see:
- ✅ Model saved to: `$GLOBAL_MODELS_DIR/llm/language_models/elephantdomain_gpt/gpt-bpe-v4-lowmem/`
- ✅ Inference test: "What is an elephant?" response
- ✅ System sleep re-enabled
- ✅ Final completion message

## 🔍 Log File Locations

```bash
# Current directory
ls -la training_log_*.txt

# Model directory  
ls -la $GLOBAL_MODELS_DIR/llm/language_models/elephantdomain_gpt/

# Tokenizer location
ls -la $GLOBAL_MODELS_DIR/llm/tokenizers/bpe-elephant/v4/
```

## 💡 Pro Tips

1. **Run overnight**: Training takes 4-6 hours, perfect for overnight runs
2. **Monitor periodically**: Use `./monitor_training.sh` to check progress
3. **Keep logs**: Logs are timestamped and never overwritten
4. **System stays awake**: Script prevents system sleep during training
5. **Safe to disconnect**: Training survives laptop closure, WiFi drops, etc.

## 🆘 Support Commands

```bash
# Complete status summary
./monitor_training.sh

# Emergency session recovery
tmux list-sessions
tmux attach-session -t $(tmux list-sessions | grep training | cut -d: -f1)

# Find all training logs
find . -name "training_log_*.txt" -mtime -7  # Last 7 days

# Disk space check (training logs can be large)
du -sh training_log_*.txt
```

---

🎯 **Ready to train your elephant domain expert GPT model!** 

Start with: `./start_training_with_logs.sh`
