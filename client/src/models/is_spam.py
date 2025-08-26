import torch
from transformers import (
    DistilBertForSequenceClassification,
    DistilBertTokenizer,
)

from settings import Settings
from settings.storage import Storage

path = Storage.base_dir / ".cache/"
model_name = "AventIQ-AI/distilbert-spam-detection"
if not (path / model_name).exists():
    ...
tokenizer = DistilBertTokenizer.from_pretrained(
    model_name,
    cache_dir=path,
    token=Settings.get_hf_token(),
)
model = DistilBertForSequenceClassification.from_pretrained(
    model_name,
    cache_dir=path,
    token=Settings.get_hf_token(),
)


def predict_spam(text: str) -> bool:
    model.eval()
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512,
    )

    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)
    return bool(torch.argmax(probs).item())
def dummy_predict_spam(text: str) -> bool:
    return False
