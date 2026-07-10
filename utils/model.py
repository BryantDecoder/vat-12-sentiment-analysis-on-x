import torch
import streamlit as st
import os
import gdown
from transformers import AutoTokenizer

from utils.model_class import IndoBERT_BiLSTM
from utils.preprocess import preprocess, load_slang_dict

MODEL_PATH = "utils/model.pt"
GDRIVE_URL = "https://drive.google.com/uc?id=17GjI3jcTnr_U_gluKIJhdDVVHIg9m0ze"

@st.cache_resource
def download_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs("utils", exist_ok=True)
        gdown.download(GDRIVE_URL, MODEL_PATH, quiet=False)

@st.cache_resource
def load_model():
    download_model()

    model = IndoBERT_BiLSTM(hidden_dim=128, output_dim=3)

    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()

    return model

@st.cache_resource
def load_tokenizer():
    return AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p1")

@st.cache_resource
def load_kamus():
    return load_slang_dict()

def predict(text):

    if text is None:
        text = ""

    text = str(text)

    model = load_model()
    tokenizer = load_tokenizer()
    kamus = load_kamus()

    text = preprocess(text, kamus)

    if not text.strip():
        text = "-"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=128
    )

    with torch.no_grad():
        outputs = model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"]
        )

        probs = torch.softmax(outputs, dim=1)
        conf, pred = torch.max(probs, dim=1)

    label_map = {
        0: "negatif",
        1: "netral",
        2: "positif"
    }

    return label_map[pred.item()], conf.item(), probs.cpu().numpy()