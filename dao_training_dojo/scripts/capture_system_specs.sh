#!/bin/bash
# scripts/capture_system_specs.sh
# Capture complete system state for reproducibility

echo "🔍 DAO Training Dojo - System Specifications"
echo "=============================================="
date
echo ""

echo "📍 LOCATION & ARCHITECTURE"
echo "Current Directory: $(pwd)"
echo "WSL Distribution: $(lsb_release -d)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo ""

echo "🐍 PYTHON ENVIRONMENT" 
echo "Python Version: $(python3 --version)"
echo "Pip Version: $(pip --version)"
echo "Virtual Environment: $VIRTUAL_ENV"
echo "Python Executable: $(which python3)"
echo ""

echo "🔧 CUDA & GPU STATUS"
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits 2>/dev/null || echo "NVIDIA GPU: Not available or not detected"
echo "CUDA Available: $(python3 -c 'import torch; print(torch.cuda.is_available())' 2>/dev/null || echo 'PyTorch not installed')"
echo "CUDA Version: $(python3 -c 'import torch; print(torch.version.cuda)' 2>/dev/null || echo 'N/A')"
echo ""

echo "📦 KEY DEPENDENCIES"
echo "PyTorch: $(python3 -c 'import torch; print(torch.__version__)' 2>/dev/null || echo 'Not installed')"
echo "Transformers: $(python3 -c 'import transformers; print(transformers.__version__)' 2>/dev/null || echo 'Not installed')"
echo "PEFT: $(python3 -c 'import peft; print(peft.__version__)' 2>/dev/null || echo 'Not installed')"
echo "Accelerate: $(python3 -c 'import accelerate; print(accelerate.__version__)' 2>/dev/null || echo 'Not installed')"
echo "BitsAndBytes: $(python3 -c 'import bitsandbytes; print(bitsandbytes.__version__)' 2>/dev/null || echo 'Not installed')"
echo "Unsloth: $(python3 -c 'from unsloth import __version__; print(__version__)' 2>/dev/null || echo 'Not installed or no version info')"
echo ""

echo "💾 STORAGE & MEMORY"
echo "Available Disk Space:"
df -h . | tail -1
echo "Memory Usage:"
free -h
echo ""

echo "📁 PROJECT STRUCTURE"
echo "Directory Contents:"
find . -maxdepth 3 -type d | head -20
echo ""
echo "Dataset Files:"
ls -la datasets/ 2>/dev/null || echo "datasets/ directory not found"
echo ""
echo "Model Config Files:"
find models/ -name "*.py" 2>/dev/null || echo "No Python files in models/ found"
echo ""

echo "🔍 ENVIRONMENT VARIABLES"
echo "PATH (first 5 entries):"
echo $PATH | tr ':' '\n' | head -5
echo "PYTHONPATH: $PYTHONPATH"
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo ""

echo "✅ VERIFICATION TESTS"
echo "Testing critical imports..."
python3 -c "
try:
    import torch
    print(f'✅ PyTorch {torch.__version__} - CUDA: {torch.cuda.is_available()}')
except: print('❌ PyTorch import failed')

try:
    import transformers
    print(f'✅ Transformers {transformers.__version__}')
except: print('❌ Transformers import failed')
    
try:
    from unsloth import FastLanguageModel
    print('✅ Unsloth import successful')
except Exception as e: print(f'❌ Unsloth import failed: {e}')

try:
    import json
    with open('datasets/dao_dataset.json', 'r') as f:
        data = json.load(f)
    print(f'✅ Dataset accessible: {len(data)} entries')
except Exception as e: print(f'❌ Dataset access failed: {e}')
"
echo ""

echo "📋 NEXT COMMANDS TO RUN"
echo "cd models/qwen_config/"
echo "python3 train_qwen_dao.py"
echo ""

echo "=============================================="
echo "Specs captured at: $(date)"
echo "Save this output to: experiments/system_specs_$(date +%Y%m%d_%H%M%S).log"