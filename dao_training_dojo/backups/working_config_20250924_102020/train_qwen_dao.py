# models/qwen_config/train_qwen_dao.py
"""
Simple Qwen DAO Trainer - Handles your messages format correctly
"""

import torch
from unsloth import FastLanguageModel
from transformers import TrainingArguments
from trl import SFTTrainer
from datasets import Dataset
import json
import logging

logger = logging.getLogger(__name__)

def main():
    """Simple training execution for messages-format data"""
    
    logging.basicConfig(level=logging.INFO)
    
    print("🔥 Starting Qwen2 Dao Training (Messages Format)...")
    print("=" * 50)
    
    # 1. Load model
    print("📥 Loading Qwen2 model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/qwen2-7b-instruct-bnb-4bit",
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )
    
    # 2. Setup LoRA
    print("🔧 Setting up LoRA...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
    )
    
    # 3. Load and convert your messages-format data
    print("📖 Loading and converting dataset...")
    with open('../../datasets/dao_dataset.json', 'r') as f:
        raw_data = json.load(f)
    
    # Convert messages format to simple instruction/output pairs
    converted_data = []
    for item in raw_data:
        messages = item["messages"]
        user_msg = ""
        assistant_msg = ""
        
        # Extract user and assistant messages
        for msg in messages:
            if msg["role"] == "user":
                user_msg = msg["content"]
            elif msg["role"] == "assistant":
                assistant_msg = msg["content"]
        
        if user_msg and assistant_msg:
            converted_data.append({
                "instruction": user_msg,
                "output": assistant_msg
            })
    
    print(f"✅ Converted {len(converted_data)} conversation pairs")
    
    # 4. Create dataset
    dataset = Dataset.from_list(converted_data)
    
    # 5. Simple formatting function
    def formatting_prompts_func(examples):
        """Format instruction/output pairs for training"""
        instructions = examples["instruction"]
        outputs = examples["output"]
        texts = []
        
        for instruction, output in zip(instructions, outputs):
            text = f"Below is an instruction. Write a response.\n\n### Instruction:\n{instruction}\n\n### Response:\n{output}<|im_end|>"
            texts.append(text)
        
        return texts
    
    # 6. Setup trainer
    print("🏃 Setting up trainer...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        formatting_func=formatting_prompts_func,
        max_seq_length=2048,
        dataset_num_proc=2,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            max_steps=60,
            learning_rate=2e-4,
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            output_dir="../../outputs/qwen_dao",
            report_to="none",
        ),
    )
    
    # 7. Train!
    print("🚀 Starting training...")
    trainer_stats = trainer.train()
    
    # 8. Save models
    print("💾 Saving models...")
    model.save_pretrained("../../outputs/qwen_dao")
    tokenizer.save_pretrained("../../outputs/qwen_dao")
    
    # Save merged version for Ollama
    print("🔄 Creating merged model for Ollama...")
    model.save_pretrained_merged("../../outputs/qwen_dao_merged", tokenizer, save_method="merged_16bit")
    
    print("\n🎉 Training completed successfully!")
    print(f"📊 Training stats: {trainer_stats}")
    print("\n📁 Outputs:")
    print("✅ Training model: ../../outputs/qwen_dao")
    print("✅ Ollama-ready model: ../../outputs/qwen_dao_merged")
    print("\n🚀 Next steps:")
    print("1. cd ../../outputs/qwen_dao_merged")
    print("2. Create Modelfile for Dao personality")
    print("3. ollama create dao_qwen -f Modelfile")

if __name__ == "__main__":
    main()