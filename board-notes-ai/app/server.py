import logging
import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image

from .model_loader import MODEL_NAME, load_model_and_processor
from .prompt_template import PROMPT_TEMPLATE

logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/generate-notes")
async def generate_notes(file: UploadFile = File(...)):
    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.") from exc

    try:
        model, processor = load_model_and_processor()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": PROMPT_TEMPLATE},
                ],
            }
        ]

        text = processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = processor(
            text=[text],
            images=[image],
            padding=True,
            return_tensors="pt",
        ).to(model.device)

        output = model.generate(**inputs, max_new_tokens=800)
        result = processor.decode(output[0], skip_special_tokens=True)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to generate board notes")
        raise HTTPException(status_code=500, detail="Failed to generate notes from the uploaded image.") from exc

    return {"notes": result}