
import sqlite3
import json
import csv
import os

try:
    from .furniture_codes import CATEGORY_CODE_TO_NAME
except ImportError:
    from furniture_codes import CATEGORY_CODE_TO_NAME


CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "decora_bedroom_dataset_v2.csv")
DB_PATH = os.path.join(os.path.dirname(__file__), "decora.db")

# Real-world approximate footprint (width, depth) in feet for each furniture
# type that appears in the dataset's furniture_list column. 

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
    "mirror": (1.0, 3.0)
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
            furniture TEXT NOT NULL,      -- JSON list of furniture name strings (no coords)
            wall_color TEXT NOT NULL,
            accent_color TEXT NOT NULL,
            estimated_cost INTEGER NOT NULL
        )
    """)

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
        try:
            _import_layouts_from_csv(cur)
            conn.commit()
        except (FileNotFoundError, csv.Error, ValueError) as e:
            print(f"[database] Skipping layout dataset import: {e}")

    conn.close()


def _extract_furniture_names(row):
    furniture_list = row.get("furniture_list")
    if furniture_list:
        return [n.strip() for n in furniture_list.split(",") if n.strip()]

    names = []
    for column, code_map in CATEGORY_CODE_TO_NAME.items():
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
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            length = float(row.get("room_length_ft") or row.get("room_length") or 0)
            width = float(row.get("room_width_ft") or row.get("room_breadth_ft") or row.get("room_width") or 0)
            style = _normalize_style(row.get("room_setup_type") or "")
            total_price = int(float(row.get("total_price_npr") or 0))

            furniture_names = _extract_furniture_names(row)

            wall_color, accent_color = STYLE_COLORS.get(style, ("Neutral White", "Warm Wood"))

            # +/-15% budget tolerance so a user's budget doesn't have to
            # match the dataset's price exactly to still be a candidate.
            min_budget = int(total_price * 0.85)
            max_budget = int(total_price * 1.15)


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
                json.dumps(furniture_names),
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
