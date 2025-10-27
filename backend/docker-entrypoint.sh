#!/bin/bash
# Docker entrypoint script for Detomo SQL AI Backend
# Automatically loads training data if needed

set -e

echo "========================================="
echo "Detomo SQL AI Backend - Starting"
echo "========================================="

# Check if training data exists
echo "Checking training data..."
TRAINING_COUNT=$(PYTHONPATH=/app python -c "
try:
    from src.detomo_vanna import DetomoVanna
    vn = DetomoVanna(config={'path': './detomo_vectordb'})
    print(len(vn.get_training_data()))
except Exception as e:
    print('0')
" 2>/dev/null || echo "0")

echo "Current training items: $TRAINING_COUNT"

# Auto-load training data if empty (for Docker only)
if [ "$TRAINING_COUNT" = "0" ] || [ "$TRAINING_COUNT" = "" ]; then
    echo "========================================="
    echo "Training data not found. Loading..."
    echo "========================================="

    if [ -f "scripts/train_chinook.py" ]; then
        PYTHONPATH=/app python scripts/train_chinook.py
        echo "✓ Training data loaded successfully"
    else
        echo "⚠ Warning: Training script not found. Skipping auto-load."
    fi
else
    echo "✓ Training data already exists ($TRAINING_COUNT items)"
fi

echo "========================================="
echo "Starting server..."
echo "========================================="

# Execute the main command (from CMD in Dockerfile)
exec "$@"
