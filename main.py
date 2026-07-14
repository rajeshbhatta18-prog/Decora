"""
DECORA - Main API
Wires together all six stages of the system architecture doc:

  1. Input Capture      -> POST /api/design
  2. Layout Engine       -> (invoked internally by /api/design and /modify)
  3. Feedback Core        -> POST /api/design/{id}/modify | /accept
  4. 2D Visualization      -> GET  /api/design/{id}/floorplan
  5. 3D Upscaling            -> POST /api/design/{id}/render3d
  6. Final Output              -> GET  /api/design/{id}
"""

import os
import socket
import uuid
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

try:
    from .models import RoomInput, ModifyRequest, SessionState, LayoutResult
    from .database import init_db, save_session, load_session_row, get_connection
    from .layout_engine import find_best_layout
    from .visualization import generate_floorplan, OUTPUT_DIR
    from .ai_render import build_3d_prompt, call_external_ai
except ImportError:
    from models import RoomInput, ModifyRequest, SessionState, LayoutResult
    from database import init_db, save_session, load_session_row, get_connection
    from layout_engine import find_best_layout
    from visualization import generate_floorplan, OUTPUT_DIR
    from ai_render import build_3d_prompt, call_external_ai

app = FastAPI(title="DECORA API", description="AI Agent for Smart Interior Design", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")


@app.on_event("startup")
def startup():
    init_db()


def _row_to_state(row) -> SessionState:
    return SessionState(
        session_id=row["session_id"],
        stage=row["stage"],
        room_input=RoomInput(**json.loads(row["room_input"])),
        current_layout=LayoutResult(**json.loads(row["current_layout"])) if row["current_layout"] else None,
        floorplan_path=row["floorplan_path"],
        render_prompt=row["render_prompt"],
    )


def _get_state_or_404(session_id: str) -> SessionState:
    row = load_session_row(session_id)
    if not row:
        raise HTTPException(status_code=404, detail="Design session not found")
    return _row_to_state(row)


# ---------------------------------------------------------------------------
# 1 & 2. INPUT CAPTURE + LAYOUT ENGINE
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 6. FINAL OUTPUT
# ---------------------------------------------------------------------------
@app.get("/api/design/{session_id}", response_model=SessionState)
def get_design(session_id: str):
    return _get_state_or_404(session_id)


@app.get("/api/layouts/seed-info")
def seed_info():
    """Quick sanity endpoint to confirm the Layout Engine DB is populated."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, room_type, style, min_budget, max_budget FROM layouts")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"count": len(rows), "layouts": rows}


@app.get("/")
def root():
    return {
        "name": "DECORA API",
        "stages": [
            "POST /api/design",
            "POST /api/design/{id}/modify",
            "POST /api/design/{id}/accept",
            "GET  /api/design/{id}/floorplan",
            "POST /api/design/{id}/verify",
            "POST /api/design/{id}/render3d",
            "GET  /api/design/{id}",
        ],
    }


def _find_available_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    requested_port = int(os.getenv("PORT", start_port))
    for port in [requested_port] + list(range(requested_port + 1, requested_port + max_attempts)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No available port found from {requested_port} to {requested_port + max_attempts - 1}")


def main():
    import uvicorn

    port = _find_available_port()
    print(f"Starting DECORA API on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
