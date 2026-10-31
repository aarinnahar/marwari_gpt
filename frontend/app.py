import streamlit as st
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Page configuration
st.set_page_config(
    page_title="Marwari LLM Chatbot", page_icon="🐪", layout="centered"
)

st.title("🐪 Marwari LLM Chatbot")
st.write(
    "Powered by your fine-tuned Llama-3.2-1B model running on Hugging Face"
    " Spaces!"
)


# Load model and tokenizer (cached so it stays in memory)
@st.cache_resource
def load_model():
  base_model_id = "meta-llama/Llama-3.2-1B-Instruct"
  adapter_id = "aarinnahar/LLama-3.2-1B-Marwari-LoRA"

  # Load tokenizer from your uploaded LoRA adapter repo
  tokenizer = AutoTokenizer.from_pretrained(adapter_id)

  # Load base model on CPU
  base_model = AutoModelForCausalLM.from_pretrained(
      base_model_id, torch_dtype=torch.float32, device_map="cpu"
  )

  # Attach your fine-tuned LoRA weights
  model = PeftModel.from_pretrained(base_model, adapter_id)
  return model, tokenizer


with st.spinner(
    "Loading fine-tuned model into memory... (This takes 1–2 mins on initial"
    " boot)"
):
  model, tokenizer = load_model()

st.success("Model loaded successfully!")

# Chat Interface
prompt = st.text_area(
    "Enter your prompt in Marwari / English:",
    placeholder="Type your message here...",
)

if st.button("Generate Response"):
  if prompt:
    with st.spinner("Generating..."):
      inputs = tokenizer(prompt, return_tensors="pt")
      outputs = model.generate(
          **inputs, max_new_tokens=150, temperature=0.7, do_sample=True
      )
      response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    st.subheader("Output:")
    st.write(response)
  else:
    st.warning("Please enter a prompt first.")
