"""Model loading utilities."""
import os
from functools import lru_cache

import torch
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

MODEL_NAME = os.getenv("BOARD_NOTES_MODEL", "Qwen/Qwen2-VL-2B-Instruct")


@lru_cache(maxsize=1)
def load_model_and_processor():
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    try:
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch_dtype,
            device_map="auto",
        )
        processor = AutoProcessor.from_pretrained(MODEL_NAME)
    except Exception as exc:
        raise RuntimeError(
            f"Unable to load model '{MODEL_NAME}'. Set BOARD_NOTES_MODEL to a smaller vision model or configure HF_TOKEN if the download is gated."
        ) from exc

    return model, processor