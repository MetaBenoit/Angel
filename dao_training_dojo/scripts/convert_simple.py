from unsloth import FastLanguageModel

# Load model with explicit device settings to avoid meta tensors
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="../outputs/qwen_dao_merged",
    dtype=None,
    load_in_4bit=False,
    device_map=None,  # Avoid device mapping that creates meta tensors
)

# Try f16 instead of q4_k_m quantization
model.save_pretrained_gguf(
    "../outputs/qwen_dao_gguf", 
    tokenizer,
    quantization_method="f16"  # Less compression, might avoid tensor issues
)
print("F16 GGUF conversion completed!")