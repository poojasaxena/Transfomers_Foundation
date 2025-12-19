#!/usr/bin/env zsh

# Helper script to start training with automatic logging
# Usage: 
#   ./start_training_with_logs.sh           # Full training
#   ./start_training_with_logs.sh --dry-run # Dry run only

set -e

# Check for dry-run flag
DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
fi

echo "🚀 Starting LLM Training with Automatic Logging"
echo "================================================"

# Generate log filename with timestamp
LOG_FILE="training_log_$(date +%Y%m%d_%H%M%S).txt"
SESSION_NAME="v4_training_$(date +%H%M%S)"

echo "📄 Log file: $LOG_FILE"
echo "🖥️  Tmux session: $SESSION_NAME"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "🔍 Running DRY RUN (validation only, no training)"
    echo "================================================"
    echo ""
    
    # Run dry-run directly in current terminal (no tmux needed)
    echo "📋 Performing validation checks..."
    ./run_training_pipeline.sh --dry-run
    
    echo ""
    echo "✅ Dry run completed!"
    echo "🚀 To start actual training: ./start_training_with_logs.sh"
else
    # Method 1: Start tmux session (logging handled by the training script itself)
    echo "🔄 Starting tmux session with logging..."
    tmux new-session -d -s "$SESSION_NAME" -c "$(pwd)" "./run_training_pipeline.sh"
fi

echo "✅ Training started in background!"
echo ""
echo "📊 To monitor:"
echo "   tmux attach-session -t $SESSION_NAME    # Attach to live session"
echo "   tail -f $LOG_FILE                       # Watch logs in real-time" 
echo "   tmux capture-pane -t $SESSION_NAME -p   # Get current screen content"
echo ""
echo "📋 Useful commands:"
echo "   tmux list-sessions                       # List all sessions"
echo "   tmux kill-session -t $SESSION_NAME      # Stop training"
echo "   grep -E '(ERROR|✅|❌|🔄)' $LOG_FILE      # Filter important events"
echo ""
echo "🎯 Training will run for ~4-6 hours. Check back later!"
