import base64
from peft import PeftModel
import streamlit as strlit
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Authenticate with Hugging Face using Streamlit Cloud Secrets
try:
  if "HF_TOKEN" in strlit.secrets:
    login(token=strlit.secrets["HF_TOKEN"])
except Exception as e:
  print(f"Login note: {e}")
    
# 1. Page Configuration
strlit.set_page_config(
    page_title="Marwari GPT | खम्मा घणी सा",
    page_icon="🐪",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Helper to load local desert background image
def set_local_background(image_file):
  try:
    with open(image_file, "rb") as f:
      encoded = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"
  except FileNotFoundError:
    return "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=2200&q=90"
      

bg_image_url = set_local_background("desert.jpg.png")

# 2. Custom CSS Styling
strlit.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    .stApp {{
        background-image: linear-gradient(
            to bottom,
            rgba(20, 15, 10, 0.40) 0%,
            rgba(40, 25, 15, 0.65) 50%,
            rgba(15, 10, 5, 0.88) 100%
        ),
        url('{bg_image_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F7F3E9;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    .hero-container {{
        text-align: center;
        padding: 2.5rem 1rem 1rem 1rem;
    }}
    .brand-title {{
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #FFD700;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 12px rgba(0,0,0,0.8);
    }}
    .hero-title {{
        font-family: 'Playfair Display', serif;
        font-size: 3.8rem;
        font-weight: 800;
        color: #FFF5E1;
        text-shadow: 0 4px 25px rgba(0,0,0,0.9);
        margin-bottom: 0.3rem;
    }}
    .hero-subtitle {{
        font-size: 1.15rem;
        font-weight: 300;
        color: #F0D4B2;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 12px rgba(0,0,0,0.7);
        margin-bottom: 1.5rem;
    }}

    .badge-container {{
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }}
    .raj-badge {{
        background: rgba(50, 30, 18, 0.85);
        border: 1px solid rgba(255, 215, 0, 0.4);
        padding: 8px 22px;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 500;
        color: #FFF0DF;
        backdrop-filter: blur(6px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }}
    .raj-badge:hover {{
        background: rgba(255, 215, 0, 0.3);
        border-color: #FFD700;
        color: #FFFFFF;
        transform: translateY(-2px);
    }}

    .chat-wrapper {{
        background: rgba(25, 15, 10, 0.82);
        border: 1px solid rgba(255, 215, 0, 0.35);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7);
        max-width: 850px;
        margin: 0 auto;
    }}

    .stChatMessage {{
        background: rgba(45, 28, 18, 0.88) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 14px !important;
        color: #FFF6EC !important;
        padding: 1rem 1.25rem !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }}
    
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stChatMessage"] div {{
        color: #FFF6EC !important;
        font-size: 1.05rem !important;
    }}

    [data-testid="stChatMessage"]:nth-child(odd) {{
        background: rgba(65, 40, 24, 0.92) !important;
        border-color: rgba(255, 215, 0, 0.45) !important;
    }}

    .stChatInputContainer textarea {{
        background-color: rgba(20, 12, 8, 0.95) !important;
        border: 1px solid #FFD700 !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    .stChatInputContainer textarea::placeholder {{
        color: #D4B291 !important;
    }}
    .stChatInputContainer textarea:focus {{
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# 3. Load Model and Tokenizer locally with caching (runs only once)
@strlit.cache_resource
def load_model():
  base_model_id = "meta-llama/Llama-3.2-1B"
  lora_model_id = "aarinnahar/Llama-3.2-1B-Marwari-LoRA"

  tokenizer = AutoTokenizer.from_pretrained(lora_model_id)
  base_model = AutoModelForCausalLM.from_pretrained(
      base_model_id, torch_dtype=torch.float16, device_map="auto"
  )
  model = PeftModel.from_pretrained(base_model, lora_model_id)
  return model, tokenizer


with strlit.spinner(
    "राजस्थानी मॉडल लोड हो रिया है... (Loading Marwari AI model into memory)"
):
  model, tokenizer = load_model()


with strlit.spinner(
    "राजस्थानी मॉडल लोड हो रिया है... (Loading Marwari AI model into memory)"
):
  model, tokenizer = load_model()


with strlit.spinner(
    "राजस्थानी मॉडल लोड हो रिया है... (Loading Marwari AI model into memory)"
):
  model, tokenizer = load_model()


# Generation Helper Function
def generate_marwari_response(prompt):
  input_text = f"User: {prompt}\nAssistant:"
  inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

  with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=250,
        temperature=0.7,
        do_sample=True,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
    )

  response = tokenizer.decode(outputs[0], skip_special_tokens=True)
  if "Assistant:" in response:
    response = response.split("Assistant:")[-1].strip()
  return response


# 4. Hero Section
strlit.markdown(
    """
    <div class="hero-container">
        <div class="brand-title">🐪 MARWARI GPT</div>
        <div class="hero-title">खम्मा घणी सा</div>
        <div class="hero-subtitle">Pick the type of Marwari intelligence & conversation that suits you best</div>
    </div>
    """,
    unsafe_allow_html=True,
)

strlit.markdown(
    """
    <div class="badge-container">
        <div class="raj-badge">🏜️ ADVENTURE CHAT</div>
        <div class="raj-badge">🏛️ ROYAL HERITAGE</div>
        <div class="raj-badge">💎 LUXURY FOLK</div>
        <div class="raj-badge">📜 MARWARI POETRY</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 5. Chat Interface
with strlit.container():
  strlit.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

  if "messages" not in strlit.session_state:
    strlit.session_state.messages = [{
        "role": "assistant",
        "content": (
            "खम्मा घणी सा! हुकम, म्हे मारवारी जीपीटी हां। आज थारे वास्ते कई सेवा"
            " कर सकूं हूँ?"
        ),
    }]

  for message in strlit.session_state.messages:
    with strlit.chat_message(
        message["role"], avatar="🐪" if message["role"] == "assistant" else "👤"
    ):
      strlit.markdown(message["content"])

  if prompt := strlit.chat_input(
      "थे कठे बारे में पूछण चाहो हो? (Ask anything in Marwari or English...)"
  ):
    strlit.session_state.messages.append({"role": "user", "content": prompt})
    with strlit.chat_message("user", avatar="👤"):
      strlit.markdown(prompt)

    with strlit.chat_message("assistant", avatar="🐪"):
      with strlit.spinner("राजस्थानी अंदाज़ में विचार कर रिया हां..."):
        response = generate_marwari_response(prompt)
        strlit.markdown(response)

    strlit.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

  strlit.markdown("</div>", unsafe_allow_html=True)
