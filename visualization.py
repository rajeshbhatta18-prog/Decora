"""
DECORA - 2D Visualization & Verification
Corresponds to Section 4 of the architecture doc.
Converts the accepted layout into a technical 2D floor plan using Matplotlib.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

try:
    from .models import RoomInput, LayoutResult
except ImportError:
    from models import RoomInput, LayoutResult

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

_FURNITURE_COLOR = "#8ecae6"
_DOOR_COLOR = "#e76f51"
_WINDOW_COLOR = "#219ebc"


def generate_floorplan(session_id: str, room: RoomInput, layout: LayoutResult) -> str:
    fig, ax = plt.subplots(figsize=(8, 8))

    # Room boundary
    ax.add_patch(Rectangle((0, 0), room.length, room.width,
                            fill=False, edgecolor="black", linewidth=2))

    # Doors
    for door in room.doors:
        _draw_wall_opening(ax, door, room, color=_DOOR_COLOR, label="Door")

    # Windows
    for window in room.windows:
        _draw_wall_opening(ax, window, room, color=_WINDOW_COLOR, label="Window")

    # Furniture
    for f in layout.furniture:
        ax.add_patch(Rectangle((f.x, f.y), f.w, f.h,
                                facecolor=_FURNITURE_COLOR, edgecolor="black",
                                alpha=0.85, linewidth=1))
        ax.text(f.x + f.w / 2, f.y + f.h / 2, f.name.replace("_", " "),
                ha="center", va="center", fontsize=8, wrap=True)

    ax.set_xlim(-1, room.length + 1)
    ax.set_ylim(-1, room.width + 1)
    ax.set_aspect("equal")
    ax.set_title(f"{layout.name} — {room.length}ft x {room.width}ft ({layout.style})")
    ax.set_xlabel("Length (ft)")
    ax.set_ylabel("Width (ft)")

    # legend (dedupe)
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc="upper right", fontsize=8)

    path = os.path.join(OUTPUT_DIR, f"{session_id}_floorplan.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def _draw_wall_opening(ax, opening, room: RoomInput, color: str, label: str):
    if opening.wall == "north":
        x0, y0 = opening.position, room.width
        ax.plot([x0, x0 + opening.width], [y0, y0], color=color, linewidth=5, label=label)
    elif opening.wall == "south":
        x0, y0 = opening.position, 0
        ax.plot([x0, x0 + opening.width], [y0, y0], color=color, linewidth=5, label=label)
    elif opening.wall == "west":
        x0, y0 = 0, opening.position
        ax.plot([x0, x0], [y0, y0 + opening.width], color=color, linewidth=5, label=label)
    elif opening.wall == "east":
        x0, y0 = room.length, opening.position
        ax.plot([x0, x0], [y0, y0 + opening.width], color=color, linewidth=5, label=label)
