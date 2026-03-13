---
title: ClassNotes AI
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "5.22.0"
app_file: app.py
pinned: false
hardware: gpu
---

# ClassNotes AI

Upload a classroom board photo → get structured study notes powered by **Qwen2-VL-2B-Instruct**.

## How it works

1. Take a photo of a whiteboard or blackboard.
2. Upload it in the Space.
3. The model reads the board and returns structured notes:
   - **Topic** · **Concepts** · **Explanation** · **Examples** · **Practice Questions**

## Deployment

Deployed automatically via GitHub Actions on every push to `main`.
See `.github/workflows/deploy.yml`.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `BOARD_NOTES_MODEL` | `Qwen/Qwen2-VL-2B-Instruct` | HuggingFace model ID |

