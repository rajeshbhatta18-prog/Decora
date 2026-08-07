import uuid
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

try:
    from .b_models import RoomInput, ModifyRequest, SessionState, LayoutResult
    from .database import init_db, save_session, load_session_row, get_connection
    from .layout_engine import find_best_layout
    from .furniture_recommender import resolve_furniture
    from .visualization import generate_floorplan, OUTPUT_DIR
    # from .image_generator import generate_image
    
except ImportError:
    from b_models import RoomInput, ModifyRequest, SessionState, LayoutResult
    from database import init_db, save_session, load_session_row, get_connection
    from layout_engine import find_best_layout
    from furniture_recommender import resolve_furniture
    from visualization import generate_floorplan, OUTPUT_DIR
    # from image_generator import generate_image  

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
@app.post("/api/design", response_model=SessionState)
def create_design(room: RoomInput):
    """Accepts user input, runs the furniture recommendation model, then
    the Layout Engine, and returns the first suggested layout."""
    resolved_furniture, notes = resolve_furniture(room)
    try:
        layout = find_best_layout(room, resolved_furniture)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    layout.warnings = notes + layout.warnings
    state = SessionState(
        session_id=str(uuid.uuid4()),
        stage="layout",
        room_input=room,
        current_layout=layout,
    )
    save_session(state)
    return state

# ---------------------------------------------------------------------------
# 3. FEEDBACK CORE
# ---------------------------------------------------------------------------
@app.post("/api/design/{session_id}/modify", response_model=SessionState)
def modify_design(session_id: str, changes: ModifyRequest):
    """Option A: Modify — updates preferences and re-runs the Layout Engine."""
    state = _get_state_or_404(session_id)

    if changes.style:
        state.room_input.style = changes.style
    if changes.budget is not None:
        state.room_input.budget = changes.budget
    if changes.required_furniture is not None:
        state.room_input.required_furniture = changes.required_furniture

    resolved_furniture, notes = resolve_furniture(state.room_input)
    try:
        state.current_layout = find_best_layout(state.room_input, resolved_furniture)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    state.current_layout.warnings = notes + state.current_layout.warnings
    state.stage = "layout"
    state.floorplan_path = None
    state.render_prompt = None
    save_session(state)
    return state


@app.post("/api/design/{session_id}/change-layout", response_model=SessionState)
def change_layout(session_id: str):

    state = _get_state_or_404(session_id)
    if not state.current_layout:
        raise HTTPException(status_code=400, detail="No layout to change yet")
    if len(state.room_input.windows) != 2:
        raise HTTPException(status_code=400, detail="Change Layout requires a room with two window walls")

    resolved_furniture, notes = resolve_furniture(state.room_input)
    try:
        state.current_layout = find_best_layout(state.room_input, resolved_furniture, swap_windows=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    state.current_layout.warnings = notes + state.current_layout.warnings
    state.stage = "layout"
    state.floorplan_path = None
    state.render_prompt = None
    save_session(state)
    return state


@app.post("/api/design/{session_id}/accept", response_model=SessionState)
def accept_design(session_id: str):

    state = _get_state_or_404(session_id)
    if not state.current_layout:
        raise HTTPException(status_code=400, detail="No layout to accept yet")

    path = generate_floorplan(session_id, state.room_input, state.current_layout)
    state.floorplan_path = path
    state.stage = "visualization"
    save_session(state)
    return state


# ---------------------------------------------------------------------------
# 4. 2D VISUALIZATION & VERIFICATION
# ---------------------------------------------------------------------------
@app.get("/api/design/{session_id}/floorplan")
def get_floorplan(session_id: str):
    state = _get_state_or_404(session_id)
    if not state.floorplan_path:
        raise HTTPException(status_code=400, detail="Floor plan not generated yet — accept a layout first")
    return FileResponse(state.floorplan_path, media_type="image/png")


@app.post("/api/design/{session_id}/verify", response_model=SessionState)
def verify_floorplan(session_id: str, approved: bool):
    state = _get_state_or_404(session_id)
    state.stage = "layout" if not approved else "verified"
    save_session(state)
    return state


# ---------------------------------------------------------------------------
# 5. 3D UPSCALING
# ---------------------------------------------------------------------------
@app.post("/api/design/{session_id}/render3d")
def render_3d(session_id: str):
    state = _get_state_or_404(session_id)

    if not state.floorplan_path:
        raise HTTPException(
            status_code=400,
            detail="Generate the floorplan first."
        )

    prompt = (
        f"Photorealistic 3D interior render of a {state.room_input.style} bedroom, "
        f"{state.room_input.length:g}ft by {state.room_input.width:g}ft, "
        f"with the approved furniture layout and a realistic premium finish."
    )

    try:
        render_path = generate_image(prompt)
        result = {
            "status": "ok",
            "message": render_path,
        }
    except Exception as exc:
        result = {
            "status": "not_configured",
            "message": str(exc),
        }

    state.render_prompt = prompt
    state.stage = "complete"
    save_session(state)
    return {
        "session": state,
        "render_result": result,
    }

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
    cur.execute("SELECT id, room_length, room_width, style, min_budget, max_budget FROM layouts")
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
            "POST /api/design/{id}/change-layout",
            "POST /api/design/{id}/accept",
            "GET  /api/design/{id}/floorplan",
            "POST /api/design/{id}/verify",
            "POST /api/design/{id}/render3d",
            "GET  /api/design/{id}",
        ],
    }


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
