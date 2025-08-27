import torch
from transformers import (
    DistilBertForSequenceClassification,
    DistilBertTokenizer,
)

from net.ai import get_spam_tracker_model
from settings.storage import Storage

tokenizer, model = None, None

def predict_spam(text: str) -> bool:
    global tokenizer, model  # noqa: PLW0603
    path = Storage.base_dir / ".cache/"
    model_name = "AventIQ-AI/distilbert-spam-detection"
    if tokenizer is None or model is None:
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
