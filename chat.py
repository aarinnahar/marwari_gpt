# 1. Install required libraries (including torchaudio to align CUDA versions)
!pip install -qU transformers accelerate torch torchvision torchaudio huggingface_hub

import torch
from transformers import pipeline

# 2. Add your Hugging Face User Access Token (starts with 'hf_...')
# Get yours at: https://huggingface.co/settings/tokens
HF_TOKEN = "YOUR-HF-TOKEN"

model_id = "aarinnahar/Marwari-Llama-3.2-1B"

print("Loading model... Please wait a moment.")

# Load pipeline with authentication token passed directly
pipe = pipeline(
    "text-generation",
    model=model_id,
    token=HF_TOKEN,
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
)

print("\nModel loaded successfully! You can start chatting below.\n" + "-"*50)

# 3. Interactive chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    messages = [
        {"role": "system", "content": "You are a helpful, concise AI assistant."},
        {"role": "user", "content": user_input},
    ]

    outputs = pipe(
        messages,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )

    assistant_response = outputs[0]["generated_text"][-1]["content"]
    print(f"\nMarwari-Llama-3.2: {assistant_response}\n" + "-"*50)
