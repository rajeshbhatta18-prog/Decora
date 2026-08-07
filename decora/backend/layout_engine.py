
from database import get_connection, STYLE_COLORS, FURNITURE_SIZES

try:
    from .b_models import RoomInput, LayoutResult, FurniturePlacement, DoorWindow
except ImportError:
    from b_models import RoomInput, LayoutResult, FurniturePlacement, DoorWindow

from layout_algo.bed import Bed
from layout_algo.wardrobe import Wardrobe
from layout_algo.table import Table
from layout_algo.chair import Chair
from layout_algo.bookshelf import Bookshelf
from layout_algo.dresser import Dresser


FURNITURE_CATEGORY = {
    "bed": "bed", "double_bed": "bed", "single_bed": "bed", "kingsize_bed": "bed",
    "wardrobe": "wardrobe", "wooden_wardrobe": "wardrobe",
    "fabric_wardrobe": "wardrobe", "hanger_wardrobe": "wardrobe",
    "table": "table", "large_table": "table", "medium_table": "table",
    "chair": "chair", "plastic_chair": "chair",
    "metal_chair": "chair", "adjustable_chair": "chair",
    "bookshelf": "bookshelf", "wooden_bookshelf": "bookshelf", "bamboo_bookshelf": "bookshelf",
    "dresser": "dresser",
    "bedside_table": None, "mirror": None, "dustbin": None,
}

_CATEGORY_DEFAULT_VARIANT = {
    "bed": "double_bed",
    "wardrobe": "wooden_wardrobe",
    "table": "medium_table",
    "chair": "plastic_chair",
    "bookshelf": "wooden_bookshelf",
    "dresser": "dresser",
}

_DEFAULT_GAPS = {
    "table": {"gap": 0.15},
    "chair": {"gap": 0.4},
    "bed": {"gap": 0.1},
    "wardrobe": {"gap": 0.1},
    "bookshelf": {"gap": 0.3, "wallgap": 0.1},
    "dresser": {"gap": 0.1, "offset": 2},
}


class _RoomRecorder:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rectangles = []

    def add_rectangle(self, x, y, w, h, label="", color="lightgray"):
        self.rectangles.append({
            "name": label,
            "x": round(x,2), 
            "y": round(y,2), 
            "w": round(w,2), 
            "h": round(h,2)
            })

    def add_line(self, *args, **kwargs):
        pass  # doors/windows are drawn separately by visualization.py

    def add_point(self, *args, **kwargs):
        pass


def _door_side(door: "DoorWindow", room_length: float, room_width: float) -> str:
    if door.wall in ("east", "west"):
        return "top" if door.position >= room_width / 2 else "bottom"
    return "right" if door.position >= room_length / 2 else "left"


def _furniture_config(category: str, selected_names):
    specific = next(
        (n for n in selected_names if FURNITURE_CATEGORY.get(n) == category and n in FURNITURE_SIZES),
        _CATEGORY_DEFAULT_VARIANT.get(category, ""),
    )
    width, height = FURNITURE_SIZES.get(specific, (2, 4))
    cfg = {"height": height, "width": width}
    cfg.update(_DEFAULT_GAPS.get(category, {"gap": 0.1}))
    return cfg, specific


def _estimate_cost(room: "RoomInput"):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT estimated_cost FROM layouts WHERE style = ? "
            "AND min_budget <= ? AND max_budget >= ? "
            "ORDER BY ABS(room_length - ?) + ABS(room_width - ?) LIMIT 1",
            (room.style, room.budget, room.budget, room.length, room.width),
        )
        row = cur.fetchone()
        if not row:
            cur.execute(
                "SELECT estimated_cost FROM layouts WHERE style = ? "
                "ORDER BY ABS(room_length - ?) + ABS(room_width - ?) LIMIT 1",
                (room.style, room.length, room.width),
            )
            row = cur.fetchone()
        conn.close()
        return int(row["estimated_cost"]) if row else None
    except Exception:
        return None


def find_best_layout(room: "RoomInput", furniture_names=None, swap_windows: bool = False) -> "LayoutResult":
    if not room.doors:
        raise ValueError("At least one door is required to run the layout engine.")

    warnings = []
    door = room.doors[0]
    if len(room.doors) > 1:
        warnings.append("The placement algorithm only supports one door; extra doors were ignored.")

    no_wind_wall = len(room.windows)
    if no_wind_wall not in (1, 2):
        raise ValueError("The layout engine needs 1 or 2 window walls specified.")

    wind_wall = room.windows[0].wall
    wind_wall2 = room.windows[1].wall if no_wind_wall == 2 else None

    if swap_windows:
        if no_wind_wall != 2:
            warnings.append("Change Layout only has an effect with two window walls; showing the same layout.")
        else:
            wind_wall, wind_wall2 = wind_wall2, wind_wall

    if door.wall == wind_wall or door.wall == wind_wall2:
        raise ValueError("Door and window cannot be on the same wall.")

    door_wall = door.wall
    door_side = _door_side(door, room.length, room.width)

    recorder = _RoomRecorder(width=room.length, height=room.width)

    if furniture_names is not None:
        selected = set(furniture_names)
    else:
        selected = set(room.required_furniture) or {"bed", "wardrobe", "table"}
    categories_selected = {FURNITURE_CATEGORY.get(n) for n in selected}

    wardrobe_cfg, wardrobe_name = _furniture_config("wardrobe", selected)
    table_cfg, table_name = _furniture_config("table", selected)
    bookshelf_cfg, bookshelf_name = _furniture_config("bookshelf", selected)
    chair_cfg, chair_name = _furniture_config("chair", selected)
    bed_cfg, bed_name = _furniture_config("bed", selected)
    dresser_cfg, dresser_name = _furniture_config("dresser", selected)

    def _place(category_name, specific_name, fn):
        before = len(recorder.rectangles)
        fn()
        added = recorder.rectangles[before:]
        if not added:
            warnings.append(f"No valid placement rule matched for '{category_name}' with this door/window layout.")
        else:
            for rect in added:
                rect["name"] = specific_name or rect["name"]

    if "table" in categories_selected:
        _place("table", table_name, lambda: Table(table_cfg).place_table(recorder, wind_wall, door_wall, door_side, bookshelf_cfg))
    if "chair" in categories_selected:
        _place("chair", chair_name, lambda: Chair(chair_cfg).place_chair(recorder, wind_wall, door_wall, door_side, table_cfg, bookshelf_cfg))
    if "bed" in categories_selected:
        _place("bed", bed_name, lambda: Bed(bed_cfg).place_bed(recorder, wind_wall, door_wall, door_side, recorder.height, recorder.width))
    if "wardrobe" in categories_selected:
        _place("wardrobe", wardrobe_name, lambda: Wardrobe(wardrobe_cfg).place_wardrobe(recorder, wind_wall, door_wall, door_side))
    if "bookshelf" in categories_selected:
        _place("bookshelf", bookshelf_name, lambda: Bookshelf(bookshelf_cfg).place_bookshelf(recorder, wind_wall, door_wall, door_side))
    if "dresser" in categories_selected:
        if recorder.height < 12 or recorder.width < 12:
            warnings.append("Room is too small for a dresser; skipped.")
        else:
            _place("dresser", dresser_name, lambda: Dresser(dresser_cfg).place_dresser(
                recorder, wind_wall, door_wall, door_side, wardrobe_cfg, bookshelf_cfg, no_wind_wall, None))

    for name in selected:
        if FURNITURE_CATEGORY.get(name) is None:
            warnings.append(f"'{name}' can not be placed in this layout.")

    wall_color, accent_color = STYLE_COLORS.get(room.style, ("Neutral White", "Warm Wood"))

    return LayoutResult(
        layout_id=1,
        name=f"{room.style.title()} Bedroom {room.length:g}x{room.width:g}ft",
        style=room.style,
        furniture=[
            FurniturePlacement(name=(r["name"] or "item").lower(), x=r["x"], y=r["y"], w=r["w"], h=r["h"])
            for r in recorder.rectangles
        ],
        wall_color=wall_color,
        accent_color=accent_color,
        match_score=1.0,
        warnings=warnings,
        estimated_cost=_estimate_cost(room),
    )
