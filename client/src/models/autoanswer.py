import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from settings import Settings
from settings.storage import Storage

tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-270m")
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-270m")


path = Storage.base_dir / ".cache/"
model_name = "google/gemma-3-270m"
if not (path / model_name).exists():
    ...

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    cache_dir=path,
    token=Settings.get_hf_token(),
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=path,
    token=Settings.get_hf_token(),
)


def generate_auto_answer(text: str) -> bool:
    model.eval()
    inputs = tokenizer(
        f"вот что тебе написали:{text}\n кратко ответь им",
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512,
    )

    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)
    return bool(torch.argmax(probs).item())


def dummy_generate_auto_answer(text: str) -> bool:
    return False
