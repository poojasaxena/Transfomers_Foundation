# TMUX 
It is used to run the large script in background

## How to run
```
# Install tmux if not already installed
sudo apt install tmux

# Create a new tmux session
tmux new-session -d -s llm_training

# Attach to the session
tmux attach-session -t llm_training

# Inside tmux, run your training
train-tokenizer experiments/v4_enhanced_pipeline/config.json
modern-gpt-train experiments/v4_enhanced_pipeline/config.json

# Detach from tmux (Ctrl+B, then D)
# Session continues running in background
```

## To Monitor Progress
```
# Reattach to see progress
tmux attach-session -t llm_training

# List all tmux sessions
tmux list-sessions

# Kill session when done
tmux kill-session -t llm_training
```

## Complete Workflow
```
# 1. Create tmux session
tmux new-session -d -s v4_training

# 2. Attach and start training
tmux attach-session -t v4_training

# 3. Inside tmux, run the complete pipeline:
./llm_training_v4.sh

# 4. Detach when needed (Ctrl+B, then D)
# 5. Reattach anytime: tmux attach-session -t v4_training
```