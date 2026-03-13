from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io

from .model_loader import load_model_and_processor
from .prompt_template import PROMPT_TEMPLATE

app = FastAPI()


@app.post("/generate-notes")
async def generate_notes(file: UploadFile = File(...)):
    model, processor = load_model_and_processor()

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

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
        add_generation_prompt=True
    )

    inputs = processor(
        text=[text],
        images=[image],
        padding=True,
        return_tensors="pt"
    ).to(model.device)

    output = model.generate(**inputs, max_new_tokens=800)

    result = processor.decode(output[0], skip_special_tokens=True)

    return {"notes": result}