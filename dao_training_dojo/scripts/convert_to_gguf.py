from unsloth import FastLanguageModel

# Load your merged model (correct relative path from scripts/)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="../outputs/qwen_dao_merged",
    dtype=None,
    load_in_4bit=False
)

# Save as GGUF for Ollama (output to parent level outputs/)
model.save_pretrained_gguf(
    "../outputs/qwen_dao_gguf", 
    tokenizer,
    quantization_method="q4_k_m"
)
print("GGUF conversion completed!")