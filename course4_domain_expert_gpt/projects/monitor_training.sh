#!/usr/bin/env zsh

# Monitor training progress
# Usage: ./monitor_training.sh

set -e

echo "🔍 Training Monitor"
echo "=================="

# Find the most recent log file
LATEST_LOG=$(ls -t training_log_*.txt 2>/dev/null | head -1)
if [ -z "$LATEST_LOG" ]; then
    echo "❌ No training logs found"
    exit 1
fi

echo "📄 Latest log: $LATEST_LOG"

# Find active tmux sessions
echo "🖥️  Active tmux sessions:"
tmux list-sessions 2>/dev/null | grep -E "(training|v4)" || echo "   No training sessions found"

echo ""
echo "📊 Recent activity (last 20 lines):"
echo "-----------------------------------"
tail -20 "$LATEST_LOG"

echo ""
echo "🎯 Quick status check:"
echo "----------------------"

# Check for key events in the log
if grep -q "Training completed successfully" "$LATEST_LOG" 2>/dev/null; then
    echo "✅ Training COMPLETED successfully!"
elif grep -q "Training failed after" "$LATEST_LOG" 2>/dev/null; then
    echo "❌ Training FAILED after all retries"
elif grep -q "Training attempt" "$LATEST_LOG" 2>/dev/null; then
    ATTEMPT=$(grep "Training attempt" "$LATEST_LOG" | tail -1)
    echo "🔄 Currently training: $ATTEMPT"
elif grep -q "Tokenizer training" "$LATEST_LOG" 2>/dev/null; then
    echo "🔤 Currently training tokenizer..."
else
    echo "🚀 Training in progress..."
fi

# Check for errors
ERROR_COUNT=$(grep -c -E "(ERROR|❌|Failed)" "$LATEST_LOG" 2>/dev/null || echo "0")
if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "⚠️  Found $ERROR_COUNT error(s) - check full log"
fi

echo ""
echo "📋 Monitor commands:"
echo "   tail -f $LATEST_LOG                     # Watch live"
echo "   grep -E '(Step|✅|❌|🔄)' $LATEST_LOG    # Key events only"
echo "   ./monitor_training.sh                   # Run this script again"
