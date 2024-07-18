from transformers import AutoTokenizer, AutoModelForCausalLM

try:
    tokenizer = AutoTokenizer.from_pretrained("KnutJaegersberg/gpt2-chatbot")
    model = AutoModelForCausalLM.from_pretrained("KnutJaegersberg/gpt2-chatbot")
    print("Model and tokenizer loaded successfully")
except Exception as e:
    print(f"Error loading model and tokenizer: {e}")
