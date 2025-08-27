import torch
from transformers import (
    DistilBertForSequenceClassification,
    DistilBertTokenizer,
)

from net.ai import get_spam_tracker_model
from settings.storage import Storage


def predict_spam(text: str) -> bool:
    path = Storage.base_dir / ".cache/"
    model_name = "AventIQ-AI/distilbert-spam-detection"
    if not (path / model_name).exists():
        get_spam_tracker_model()
    tokenizer = DistilBertTokenizer.from_pretrained(
    model_name,
    cache_dir=path,
    )
    model = DistilBertForSequenceClassification.from_pretrained(
        model_name,
        cache_dir=path,
    )
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
