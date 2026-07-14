"""
DECORA - 3D Upscaling
Corresponds to Section 5: 3D UPSCALING in the system architecture doc.

This module was referenced by main.py (POST /api/design/{id}/render3d) but
was missing from the files provided, which crashed the whole app at
startup with ModuleNotFoundError.

build_3d_prompt() turns the accepted 2D layout into a natural-language
prompt suitable for a text-to-image / text-to-3D model.

call_external_ai() is intentionally a thin, swappable wrapper: no specific
provider (Stability, Replicate, Meshy, OpenAI, etc.) was specified anywhere
else in the codebase, so this doesn't hardcode a guess at one. Configure it
via the two environment variables below; without them it returns a clear
"not configured" response instead of crashing the request.
"""

import os
import requests

try:
    from .models import RoomInput, LayoutResult
except ImportError:
    from models import RoomInput, LayoutResult

RENDER_API_URL = os.environ.get("DECORA_RENDER_API_URL")
RENDER_API_KEY = os.environ.get("DECORA_RENDER_API_KEY")


def build_3d_prompt(room: RoomInput, layout: LayoutResult) -> str:
    furniture_desc = ", ".join(
        f"{f.name.replace('_', ' ')} ({f.w:g}ft x {f.h:g}ft)" for f in layout.furniture
    )
    return (
        f"Photorealistic 3D interior render of a {room.length:g}ft x {room.width:g}ft "
        f"{room.room_type.replace('_', ' ')} in {layout.style} style. "
        f"Wall color: {layout.wall_color}, accent color: {layout.accent_color}. "
        f"Furniture: {furniture_desc}. "
        f"Natural lighting, eye-level camera angle, high detail."
    )


def call_external_ai(prompt: str) -> dict:
    """
    Sends `prompt` to whatever external render provider is configured.
    Returns a dict describing the outcome; never raises, so a missing/failed
    provider degrades gracefully instead of taking down /render3d.
    """
    if not RENDER_API_URL or not RENDER_API_KEY:
        return {
            "status": "not_configured",
            "message": (
                "No 3D render provider is configured. Set DECORA_RENDER_API_URL "
                "and DECORA_RENDER_API_KEY to enable this step."
            ),
            "prompt": prompt,
        }

    try:
        resp = requests.post(
            RENDER_API_URL,
            headers={"Authorization": f"Bearer {RENDER_API_KEY}"},
            json={"prompt": prompt},
            timeout=30,
        )
        resp.raise_for_status()
        return {"status": "ok", "provider_response": resp.json()}
    except requests.RequestException as e:
        return {"status": "error", "message": str(e), "prompt": prompt}
