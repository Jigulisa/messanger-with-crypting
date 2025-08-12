import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer

from settings.storage import Storage

path = Storage.base_dir / ".cache/"
model_name = "AventIQ-AI/distilbert-spam-detection"
tokenizer = DistilBertTokenizer.from_pretrained(model_name, cache_dir=path)
model = DistilBertForSequenceClassification.from_pretrained(model_name, cache_dir=path)


def predict_spam(text):
    model.eval()
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512,
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        pred_class = torch.argmax(probs).item()
    return pred_class
