"""Model loading utilities."""
from functools import lru_cache

import torch
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct"


@lru_cache(maxsize=1)
def load_model_and_processor():
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch_dtype,
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained(MODEL_NAME)

    return model, processor