import torch
from transformers import GPT2Tokenizer, T5ForConditionalGeneration

from settings import Settings
from settings.storage import Storage

path = Storage.base_dir / ".cache/"
model_name = "RussianNLP/FRED-T5-Summarizer"
if not (path / model_name).exists():
    ...
tokenizer = GPT2Tokenizer.from_pretrained(
    "RussianNLP/FRED-T5-Summarizer",
    eos_token="</s>",  # noqa: S106
    token=Settings.get_hf_token(),
)
model = T5ForConditionalGeneration.from_pretrained(
    "RussianNLP/FRED-T5-Summarizer",
    token=Settings.get_hf_token(),
)


def summarizer(data: str) -> str:
    input_text = f"<LM> Сократи текст.\n {data}"
    input_ids = torch.tensor([tokenizer.encode(input_text)])
    outputs = model.generate(
        input_ids,
        eos_token_id=tokenizer.eos_token_id,
        num_beams=5,
        min_new_tokens=17,
        max_new_tokens=200,
        do_sample=True,
        no_repeat_ngram_size=4,
        top_p=0.9,
    )
    return tokenizer.decode(outputs[0][1:])
