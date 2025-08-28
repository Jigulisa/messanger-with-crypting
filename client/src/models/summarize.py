import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from net.ai import get_summarization_model
from settings.storage import Storage


def summarizer(data: str) -> str:
    path = Storage.base_dir / ".cache/"
    model_name = "Paleontolog/bart_rus_summarizer"
    if not (path / model_name).exists():
        get_summarization_model()
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=path,
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        cache_dir=path,
    )
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
