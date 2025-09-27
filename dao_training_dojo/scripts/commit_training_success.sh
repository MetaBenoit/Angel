#!/bin/bash
# scripts/commit_training_success.sh
# Commit the successful training configuration

echo "🎉 Committing DAO Training Success Recipe"
echo "========================================"

# Navigate to project root
cd /mnt/c/Users/benyr/Angel/dao_training_dojo/

# Create success documentation
echo "📝 Creating success documentation..."
cat > TRAINING_SUCCESS.md << 'EOF'
# 🏆 DAO TRAINING SUCCESS - Secret Recipe

**Date:** $(date)
**Status:** ✅ WORKING PERFECTLY
**Model:** Qwen2-7B with Unsloth acceleration

## The Key Breakthrough
The `formatting_func` in Unsloth must return a **list of strings directly**, not a dictionary!

```python
# ❌ WRONG:
return {"text": texts}

# ✅ CORRECT:
return texts
```

## Working Configuration
- Model: unsloth/qwen2-7b-instruct-bnb-4bit
- Dataset: 277 conversation pairs in messages format
- Training: 60 steps, ~10 minutes
- Output: Fully trained Dao personality

## Files That Work
- `models/qwen_config/train_qwen_dao.py` - The magic script
- `datasets/dao_dataset.json` - Messages format data
- `outputs/qwen_dao_merged/` - Ollama-ready model

## Next Steps
1. Create Modelfile for Dao personality
2. Deploy with ollama create dao_qwen -f Modelfile
3. Test with web interface

**Recipe locked in!** 🔐
EOF

# Capture exact system state
echo "🔍 Capturing system specifications..."
bash scripts/capture_system_specs.sh > experiments/training_success_$(date +%Y%m%d_%H%M%S).log

# Create backup of working files
echo "💾 Creating backups of critical files..."
mkdir -p backups/working_config_$(date +%Y%m%d_%H%M%S)/

# Backup the working script
cp models/qwen_config/train_qwen_dao.py backups/working_config_$(date +%Y%m%d_%H%M%S)/
cp datasets/dao_dataset.json backups/working_config_$(date +%Y%m%d_%H%M%S)/

# List what we've got
echo "📁 Current project structure:"
find . -type f -name "*.py" -o -name "*.json" -o -name "*.md" | head -20

echo ""
echo "✅ SUCCESS COMMITTED!"
echo "📍 Key files preserved:"
echo "   - TRAINING_SUCCESS.md (methodology)"
echo "   - models/qwen_config/train_qwen_dao.py (working script)"
echo "   - experiments/training_success_*.log (system state)"
echo "   - backups/working_config_*/ (file backups)"
echo ""
echo "🚀 Ready for next phase: Ollama deployment!"

# Show outputs directory
echo "📦 Training outputs:"
ls -la outputs/ 2>/dev/null || echo "Run training first to generate outputs"