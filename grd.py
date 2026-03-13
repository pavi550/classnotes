import gradio as gr
import os
import requests

API_BASE_URL = os.getenv("BOARD_NOTES_API_BASE_URL", "http://127.0.0.1:8000")
API_URL = f"{API_BASE_URL.rstrip('/')}/generate-notes"
HEALTH_URL = f"{API_BASE_URL.rstrip('/')}/health"

def generate_notes(image):
    try:
        health_response = requests.get(HEALTH_URL, timeout=5)
        health_response.raise_for_status()
    except requests.RequestException:
        return "Backend is unavailable. Start the API with: cd board-notes-ai && .venv/bin/python -m uvicorn app.server:app --host 127.0.0.1 --port 8000"

    try:
        with open(image, "rb") as image_file:
            response = requests.post(API_URL, files={"file": image_file}, timeout=(10, 600))

        response.raise_for_status()
        payload = response.json()
        return payload.get("notes", "The API responded without generated notes.")
    except requests.HTTPError:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        return f"Backend request failed: {detail}"
    except requests.RequestException as exc:
        return f"Request to backend failed: {exc}"

interface = gr.Interface(
    fn=generate_notes,
    inputs=gr.Image(type="filepath"),
    outputs="text",
    title="Board Notes Generator"
)

if __name__ == "__main__":
    interface.launch()
