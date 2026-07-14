"""
DECORA - Database Layer
Corresponds to the "Decora Database" referenced in Section 2: LAYOUT ENGINE,
and the session persistence needed to drive the Feedback Core loop (Section 3).

Uses SQLite, per the TECHNOLOGY STACK section of the architecture doc.

This version loads the "layouts" table from a REAL dataset
(data/decora_bedroom_dataset_v2.csv) instead of hand-written examples.
That CSV lists, for each of ~2244 real bedroom layouts: room size, style,
budget, and which furniture items are present -- but it does NOT include
exact x/y coordinates for each piece of furniture. So this file also does
the job of turning a furniture *list* (e.g. "bed, desk, chair") into actual
placed rectangles (x, y, width, height) using a simple packing algorithm,
explained below in _place_furniture().
"""

import sqlite3
import json
import csv
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "decora.db")
# CSV_PATH = pd.read_csv("E:\second_sem_project\Main Decora Code\datasets\interior_design_dataset_bedroom.csv")
CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "datasets",
    "interior_design_dataset_bedroom.csv",)

# Real-world approximate footprint (width, depth) in feet for each furniture
# type that appears in the dataset's furniture_list column. Anything not
# listed here falls back to a generic 1.5ft x 1.5ft footprint.
FURNITURE_SIZES = {
    "double_bed": (4.0, 6),
    "single_bed": (3.0, 6),
    "kingsize_bed": (6.0, 6.0),
    "wooden_wardrobe": (2.5, 4.0),
    "fabric_wardrobe": (2.0, 4.0),
    "hanger_wardrobe": (2.0, 4.0),
    "dresser": (1.8, 5.0),
    "large_table": (2.0, 4.0),
    "medium_table": (2.0, 3.0),
    "plastic_chair": (1.5, 1.85),
    "metal_chair": (1.5, 1.5),
    "adjustable_chair": (1.8, 2.0),
    "wooden_bookshelf": (1.0, 3.0),
    "bamboo_bookshelf": (1.0, 3.0),
    "bedside_table": (1.5, 2.0),
    "dustbin": (1.0, 1.0),
    "mirror": (1.0, 3.0),

} 

# The dataset doesn't include wall/accent colors, so we pick a sensible
# palette per style (matches the "style-based color combos" idea from
# the presentation doc's "Types of Design Assistance" slide).
STYLE_COLORS = {    
    "luxury": ("Deep Charcoal", "Brushed Gold"),
    "standard": ("Neutral White", "Sage Green"),
    "budget": ("Off White", "Slate Blue")
}
    


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS layouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_length REAL NOT NULL,
            room_width REAL NOT NULL,
            style TEXT NOT NULL,
            min_budget INTEGER NOT NULL,
            max_budget INTEGER NOT NULL,
            furniture TEXT NOT NULL,      -- JSON list of FurniturePlacement dicts
            wall_color TEXT NOT NULL,
            accent_color TEXT NOT NULL,
            estimated_cost INTEGER NOT NULL
        )
    """)

    # Handle existing databases created before the style column existed.
    # try:
    #     cur.execute("SELECT style FROM layouts LIMIT 1")
    # except sqlite3.OperationalError:
    #     cur.execute("ALTER TABLE layouts ADD COLUMN style TEXT NOT NULL DEFAULT 'standard'")

    # name TEXT NOT NULL,
    # style TEXT NOT NULL,

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            stage TEXT NOT NULL,
            room_input TEXT NOT NULL,      -- JSON
            current_layout TEXT,           -- JSON
            floorplan_path TEXT,
            render_prompt TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    cur.execute("SELECT COUNT(*) as c FROM layouts")
    if cur.fetchone()["c"] == 0:
        _import_layouts_from_csv(cur)
        conn.commit()

    conn.close()


def _place_furniture(names, room_l, room_w):
#     """
#     Turns a list of furniture NAMES (no coordinates) into a list of placed
#     rectangles that fit inside a room_l x room_w foot room.

#     How it works (like arranging boxes on a shelf, wrapping to a new row
#     when you run out of space):
#       1. Start at the top-left corner (with a small margin from the walls).
#       2. Place each item, then move the "cursor" to the right by that
#          item's width.
#       3. If the next item would go past the right wall, wrap down to a
#          new row (reset x, move y down by the tallest item in that row).
#       4. Rugs are handled separately -- in real rooms a rug sits UNDER
#          other furniture, so it's centered on the floor instead of taking
#          up its own slot in the packing order.
#     """
    margin = 0.5
    cur_x, cur_y, row_h = margin, margin, 0.0
    placements = []

    # for name in names:
    #     if name == "rug":
    #         continue
    #     w, h = FURNITURE_SIZES.get(name, (1.5, 1.5))
    #     w = min(w, max(room_l - 2 * margin, 0.5))
    #     h = min(h, max(room_w - 2 * margin, 0.5))

    #     if cur_x + w > room_l - margin:
    #         cur_x = margin
    #         cur_y += row_h + margin
    #         row_h = 0.0

    #     placements.append({
    #         "name": name,
    #         "x": round(cur_x, 2), "y": round(cur_y, 2),
    #         "w": round(w, 2), "h": round(h, 2),
    #         "rotation": 0,
    #     })
    #     cur_x += w + margin
    #     row_h = max(row_h, h)

    # if "rug" in names:
    #     w, h = FURNITURE_SIZES["rug"]
    #     w = min(w, max(room_l - 1, 1))
    #     h = min(h, max(room_w - 1, 1))
    #     placements.append({
    #         "name": "rug",
    #         "x": round((room_l - w) / 2, 2), "y": round(margin, 2),
    #         "w": round(w, 2), "h": round(h, 2),
    #         "rotation": 0,
    #     })

    # return placements


def _extract_furniture_names(row):
    furniture_list = row.get("furniture_list")
    if furniture_list:
        return [n.strip() for n in furniture_list.split(",") if n.strip()]

    mapping = {
        "bed": {"db": "double_bed", "sb": "single_bed"},
        "table": {"lt": "large_table", "mt": "medium_table"},
        "chair": {"pc": "plastic_chair", "mc": "metal_chair"},
        "wardrobe": {"fw": "fabric_wardrobe", "hw_wardrobe": "hanger", "ww": "wooden_wardrobe"},
        "bookshelf": {"wb": "wooden_bookshelf", "bb": "bamboo_bookshelf"},
        "bedsidetable": {"bt": "bedside_table"},
        "dresser": {"dr": "dresser"},
    }

    names = []
    for column, code_map in mapping.items():
        value = (row.get(column) or "").strip()
        if not value or value.upper() == "NA":
            continue
        mapped = code_map.get(value.lower())
        if mapped:
            names.append(mapped)
    return names


def _normalize_style(style: str) -> str:
    style = (style or "").strip().lower()
    return {"standard": "standard", "budget": "budget", "luxury": "luxury"}.get(style, style)


def _import_layouts_from_csv(cur):
    """
    Reads the bedroom dataset and inserts one row per layout into the layouts
    table, computing furniture placement for each.
    """
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            length = float(row.get("room_length_ft") or row.get("room_length") or 0)
            width = float(row.get("room_width_ft") or row.get("room_breadth_ft") or row.get("room_width") or 0)
            style = _normalize_style(row.get("room_setup_type") or "")
            total_price = int(float(row.get("total_price_npr") or 0))

            furniture_names = _extract_furniture_names(row)
            furniture = _place_furniture(furniture_names, length, width)

            wall_color, accent_color = STYLE_COLORS.get(style, ("Neutral White", "Warm Wood"))

            # +/-15% budget tolerance so a user's budget doesn't have to
            # match the dataset's price exactly to still be a candidate.
            min_budget = int(total_price * 0.85)
            max_budget = int(total_price * 1.15)

            # name = f"{style.title()} Bedroom {length:g}x{width:g}ft (#{i + 1})"

            cur.execute("""
                INSERT INTO layouts
                (room_length, room_width, style,
                 min_budget, max_budget, furniture, wall_color, accent_color, estimated_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                length,
                width,
                style,
                min_budget,
                max_budget,
                json.dumps(furniture),
                wall_color,
                accent_color,
                total_price,
            ))


def save_session(state) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sessions (session_id, stage, room_input, current_layout, floorplan_path, render_prompt, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(session_id) DO UPDATE SET
            stage=excluded.stage,
            room_input=excluded.room_input,
            current_layout=excluded.current_layout,
            floorplan_path=excluded.floorplan_path,
            render_prompt=excluded.render_prompt,
            updated_at=CURRENT_TIMESTAMP
    """, (
        state.session_id, state.stage, state.room_input.model_dump_json(),
        state.current_layout.model_dump_json() if state.current_layout else None,
        state.floorplan_path, state.render_prompt,
    ))
    conn.commit()
    conn.close()


def load_session_row(session_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
    row = cur.fetchone()
    conn.close()
    return row
