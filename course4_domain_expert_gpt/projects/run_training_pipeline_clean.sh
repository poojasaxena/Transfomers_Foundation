#!/usr/bin/env zsh

# Robust LLM Training Script with Auto-Recovery
# 
# How to run:
# 1. Copy to your learning project directory
# 2. cd "$LEARNING_ROOT/NLP_and_LLMs/Transfomers_Foundation/course4_doecho "🔤 Step 1: Checking tokenizer..."

# Reuse the tokenizer path and status from dry-run check
echo "🔍 Tokenizer path: $TOKENIZER_PATH"
echo "📁 File check result:"
ls -la "$TOKENIZER_PATH" 2>/dev/null || echo "   ❌ File not found at expected path"

if [ "$TOKENIZER_EXISTS" = "true" ]; then
    echo "✅ Tokenizer already exists: $TOKENIZER_PATH"
    echo "🚀 Skipping tokenizer training..."jects"
# 3. chmod +x run_training_pipeline.sh
# 4. tmux new-session -d -s v4_training
# 5. tmux attach-session -t v4_training
# 6. ./run_training_pipeline.sh
# 
# Features:
# - Comprehensive dry-run with path validation
# - Smart tokenizer check (skips if exists)
# - Robust training with auto-retry (3 attempts)
# - Interactive confirmation before execution
# - System sleep prevention during training

set -e

echo "🤖 Starting Robust LLM Training Pipeline V4..."
echo "📅 Started at: $(date)"
echo "🖥️  Host: $(hostname)"
echo "💾 Available space: $(df -h . | tail -1 | awk '{print $4}')"

# Prevent system sleep during training
echo "🔒 Preventing system sleep..."
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target 2>/dev/null || true

# Keep WiFi active
echo "📡 Configuring WiFi to stay active..."
sudo iwconfig wlan0 power off 2>/dev/null || true

# Verify environment variables
echo "🔧 Using GLOBAL_DATASETS_DIR: $GLOBAL_DATASETS_DIR"
echo "🔧 Using LEARNING_ROOT: $LEARNING_ROOT"

# Change to learning project directory
PROJECT_DIR="$LEARNING_ROOT/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects"
echo "📁 Changing to project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

# Set config path relative to project directory
CONFIG_PATH="4_elephant_twicedata/config_low_memory.json"

# === DRY RUN: Check everything before proceeding ===
echo ""
echo "🔍 === DRY RUN: Checking all paths and dependencies ==="
echo ""

# Check config file
if [ -f "$CONFIG_PATH" ]; then
    echo "✅ Config file found: $CONFIG_PATH"
else
    echo "❌ Config file NOT found: $CONFIG_PATH"
    echo "📍 Current directory: $(pwd)"
    echo "📋 Available configs:"
    find . -name "*.json" -type f 2>/dev/null || echo "   No JSON files found"
    exit 1
fi

# Extract paths from config
PATHS=$(python3 -c "
import json, os
try:
    with open('$CONFIG_PATH', 'r') as f:
        config = json.load(f)
    
    # Extract key paths
    pm = config['project_metadata']
    tokenizer_path = pm['tokenizer_save_path']
    model_path = pm['model_save_path']
    data_path = pm['data_path']
    
    # Handle relative paths
    if not tokenizer_path.startswith('/') and 'GLOBAL_DATASETS_DIR' in os.environ:
        tokenizer_path = os.path.join(os.environ['GLOBAL_DATASETS_DIR'], tokenizer_path)
    if not model_path.startswith('/') and 'GLOBAL_DATASETS_DIR' in os.environ:
        model_path = os.path.join(os.environ['GLOBAL_DATASETS_DIR'], model_path)
    if not data_path.startswith('/') and 'GLOBAL_DATASETS_DIR' in os.environ:
        data_path = os.path.join(os.environ['GLOBAL_DATASETS_DIR'], data_path)
    
    print(f'TOKENIZER_PATH={tokenizer_path}')
    print(f'MODEL_PATH={model_path}')
    print(f'DATA_PATH={data_path}')
    print(f'TRAIN_FILE={os.path.join(data_path, pm[\"data_file\"])}')
    print(f'VAL_FILE={os.path.join(data_path, pm[\"val_file\"])}')
    
except Exception as e:
    print(f'ERROR={e}')
" 2>/dev/null)

if [[ "$PATHS" == *"ERROR="* ]]; then
    echo "❌ Failed to parse config file"
    echo "$PATHS"
    exit 1
fi

# Parse the paths
eval "$PATHS"

echo "📂 Key Paths Check:"
echo "   Tokenizer: $TOKENIZER_PATH"
echo "   🔍 Debug: Checking file existence..."
ls -la "$TOKENIZER_PATH" 2>/dev/null && echo "   📄 File found!" || echo "   ❌ File not found!"
if [ -f "$TOKENIZER_PATH" ]; then
    echo "   ✅ Tokenizer EXISTS"
    TOKENIZER_EXISTS=true
else
    echo "   🔧 Tokenizer MISSING (will be trained)"
    echo "   🐛 Debug info:"
    echo "      - Path: '$TOKENIZER_PATH'"
    echo "      - Directory exists: $([ -d "$(dirname "$TOKENIZER_PATH")" ] && echo "YES" || echo "NO")"
    echo "      - Directory contents:"
    ls -la "$(dirname "$TOKENIZER_PATH")" 2>/dev/null || echo "      Directory not accessible"
    TOKENIZER_EXISTS=false
fi

echo "   Model save: $MODEL_PATH"
if [ -d "$MODEL_PATH" ]; then
    echo "   📁 Model directory EXISTS"
else
    echo "   📁 Model directory MISSING (will be created)"
fi

echo "   Training data: $TRAIN_FILE"
if [ -f "$TRAIN_FILE" ]; then
    TRAIN_SIZE=$(wc -l < "$TRAIN_FILE" 2>/dev/null || echo "unknown")
    echo "   ✅ Training data EXISTS ($TRAIN_SIZE lines)"
else
    echo "   ❌ Training data MISSING"
    exit 1
fi

echo "   Validation data: $VAL_FILE"
if [ -f "$VAL_FILE" ]; then
    VAL_SIZE=$(wc -l < "$VAL_FILE" 2>/dev/null || echo "unknown")
    echo "   ✅ Validation data EXISTS ($VAL_SIZE lines)"
else
    echo "   ❌ Validation data MISSING"
    exit 1
fi

echo ""
echo "🎯 What will happen:"
if [ "$TOKENIZER_EXISTS" = "true" ]; then
    echo "   1️⃣ Skip tokenizer training (already exists)"
else
    echo "   1️⃣ Train new tokenizer → $TOKENIZER_PATH"
fi
echo "   2️⃣ Train model → $MODEL_PATH"
echo "   3️⃣ Test inference with sample prompt"
echo ""
echo "⏱️  Estimated time: 4-6 hours for model training"
echo "🔒 System sleep will be disabled during training"
echo "📡 WiFi power management will be disabled"
echo ""

# Interactive confirmation
echo "🤔 Do you want to proceed with training? (y/n)"
read -r PROCEED
if [[ ! "$PROCEED" =~ ^[Yy]$ ]]; then
    echo "🚫 Training cancelled by user"
    exit 0
fi

echo ""
echo "🚀 Starting training pipeline..."
echo "======================================="

# Function to check if process is running
check_gpu_memory() {
    nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null || echo "0"
}

# Function to monitor and restart if needed
robust_train() {
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        echo "🔄 Training attempt $((retry_count + 1))..."
        
        # Run training with timeout and error handling
        if timeout 8h modern-gpt-train "$CONFIG_PATH"; then
            echo "✅ Training completed successfully!"
            break
        else
            echo "⚠️ Training failed or timed out (attempt $((retry_count + 1)))"
            retry_count=$((retry_count + 1))
            
            if [ $retry_count -lt $max_retries ]; then
                echo "🔄 Retrying in 30 seconds..."
                sleep 30
            fi
        fi
    done
    
    if [ $retry_count -eq $max_retries ]; then
        echo "❌ Training failed after $max_retries attempts"
        return 1
    fi
}

# Step 1: Smart tokenizer training (check if exists first)
echo ""
echo "🔤 Step 1: Checking tokenizer..."

# Extract tokenizer path from config
TOKENIZER_PATH=$(python3 -c "
import json
with open('$CONFIG_PATH', 'r') as f:
    config = json.load(f)
tokenizer_path = config['project_metadata']['tokenizer_save_path']
if not tokenizer_path.startswith('/'):
    # Handle relative paths
    import os
    if 'GLOBAL_DATASETS_DIR' in os.environ:
        tokenizer_path = os.path.join(os.environ['GLOBAL_DATASETS_DIR'], tokenizer_path)
print(tokenizer_path)
" 2>/dev/null || echo "")

if [ -n "$TOKENIZER_PATH" ] && [ -f "$TOKENIZER_PATH" ]; then
    echo "✅ Tokenizer already exists: $TOKENIZER_PATH"
    echo "� Skipping tokenizer training..."
else
    echo "🔧 Tokenizer not found, training new one..."
    train-tokenizer "$CONFIG_PATH"
    echo "✅ Tokenizer training completed at: $(date)"
fi

# Step 2: Robust model training
echo "🧠 Step 2: Starting robust model training..."
echo "💡 Training will auto-retry up to 3 times if it fails"
echo "⏱️  Max training time: 8 hours with timeout"

robust_train

# Step 3: Test inference
echo "🎯 Step 3: Testing inference..."
echo "What is an elephant?" | modern-gpt-infer "$CONFIG_PATH"

# Cleanup: Re-enable sleep
echo "🔓 Re-enabling system sleep..."
sudo systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target 2>/dev/null || true

echo "✅ Training completed at: $(date)"
echo "🎉 Robust LLM Training V4 Complete!"
