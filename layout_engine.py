"""
DECORA - Layout Engine
Corresponds to Section 2: LAYOUT ENGINE in the system architecture doc.

Responsibilities (from the doc):
- Searches layouts matching room dimensions
- Applies architectural rules and constraints
- Places furniture according to spacing rules
- Filters layouts based on user style and budget
- Selects the most suitable recommendation
"""

import json
from typing import List

try:
    from .database import get_connection
    from .models import RoomInput, LayoutResult, FurniturePlacement
except ImportError:
    from database import get_connection
    from models import RoomInput, LayoutResult, FurniturePlacement


def _dimension_score(room: RoomInput, tmpl_l: float, tmpl_w: float) -> float:
    """1.0 = perfect match, decays as aspect ratio / size diverge."""
    room_ratio = room.length / room.width
    tmpl_ratio = tmpl_l / tmpl_w
    ratio_diff = abs(room_ratio - tmpl_ratio) / max(room_ratio, tmpl_ratio)

    room_area = room.length * room.width
    tmpl_area = tmpl_l * tmpl_w
    area_diff = abs(room_area - tmpl_area) / max(room_area, tmpl_area)

    return max(0.0, 1.0 - (0.6 * ratio_diff + 0.4 * area_diff))


def _budget_score(user_budget: int, min_b: int, max_b: int) -> float:
    if min_b <= user_budget <= max_b:
        return 1.0
    # graceful falloff if outside range
    if user_budget < min_b:
        gap = (min_b - user_budget) / max(min_b, 1)
    else:
        gap = (user_budget - max_b) / max(max_b, 1)
    return max(0.0, 1.0 - gap)


def _furniture_coverage_score(required: List[str], available_names: List[str]) -> float:
    if not required:
        return 1.0
    required_lc = [r.lower().replace(" ", "_") for r in required]
    available_lc = [a.lower() for a in available_names]
    hits = sum(1 for r in required_lc if any(r in a or a in r for a in available_lc))
    return hits / len(required_lc)


def _scale_furniture(furniture: list, tmpl_l: float, tmpl_w: float,
                      room_l: float, room_w: float) -> List[FurniturePlacement]:
    scale_x = room_l / tmpl_l
    scale_y = room_w / tmpl_w
    scaled = []
    for f in furniture:
        scaled.append(FurniturePlacement(
            name=f["name"],
            x=round(f["x"] * scale_x, 2),
            y=round(f["y"] * scale_y, 2),
            w=round(f["w"] * scale_x, 2),
            h=round(f["h"] * scale_y, 2),
            rotation=f.get("rotation", 0),
        ))
    return scaled


def _check_clearance(room: RoomInput, furniture: List[FurniturePlacement]) -> List[str]:
    """
    Simplified architectural rule check: flags furniture that blocks a
    door/window opening. Keeps a 2.5ft clearance zone in front of each door.
    """
    warnings = []
    for door in room.doors:
        for f in furniture:
            if door.wall in ("north", "south"):
                door_x_start, door_x_end = door.position, door.position + door.width
                blocking_y = f.y < 2.5 if door.wall == "north" else f.y + f.h > room.width - 2.5
                overlapping_x = not (f.x + f.w < door_x_start or f.x > door_x_end)
                if blocking_y and overlapping_x:
                    warnings.append(f"{f.name} may block clearance for the {door.wall} door.")
            else:  # east/west
                door_y_start, door_y_end = door.position, door.position + door.width
                blocking_x = f.x < 2.5 if door.wall == "west" else f.x + f.w > room.length - 2.5
                overlapping_y = not (f.y + f.h < door_y_start or f.y > door_y_end)
                if blocking_x and overlapping_y:
                    warnings.append(f"{f.name} may block clearance for the {door.wall} door.")

    for f in furniture:
        if f.x + f.w > room.length + 0.01 or f.y + f.h > room.width + 0.01:
            warnings.append(f"{f.name} may extend beyond room boundary after scaling — consider a smaller variant.")

    return warnings


def find_best_layout(room: RoomInput) -> LayoutResult:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM layouts WHERE room_type = ?", (room.room_type,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        raise ValueError(f"No layouts available for room_type='{room.room_type}'")

    scored = []
    for row in rows:
        furniture = json.loads(row["furniture"])
        style_score = 1.0 if row["style"] == room.style else 0.4
        dim_score = _dimension_score(room, row["room_length"], row["room_width"])
        budget_score = _budget_score(room.budget, row["min_budget"], row["max_budget"])
        coverage_score = _furniture_coverage_score(
            room.required_furniture, [f["name"] for f in furniture]
        )
        total = (0.30 * dim_score + 0.30 * style_score +
                 0.25 * budget_score + 0.15 * coverage_score)
        scored.append((total, row))

    scored.sort(key=lambda t: t[0], reverse=True)
    best_score, best_row = scored[0]

    furniture_raw = json.loads(best_row["furniture"])
    scaled_furniture = _scale_furniture(
        furniture_raw, best_row["room_length"], best_row["room_width"],
        room.length, room.width
    )
    warnings = _check_clearance(room, scaled_furniture)

    return LayoutResult(
        layout_id=best_row["id"],
        name=best_row["name"],
        style=best_row["style"],
        furniture=scaled_furniture,
        wall_color=best_row["wall_color"],
        accent_color=best_row["accent_color"],
        match_score=round(best_score, 3),
        warnings=warnings,
        estimated_cost=best_row["estimated_cost"],
    )
