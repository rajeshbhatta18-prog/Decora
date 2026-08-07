import os
import sys
from typing import List, Tuple

try:
    from .b_models import RoomInput
    from .furniture_codes import NAME_TO_CATEGORY, CATEGORY_CODE_TO_NAME
except ImportError:
    from b_models import RoomInput
    from furniture_codes import NAME_TO_CATEGORY, CATEGORY_CODE_TO_NAME

_ML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ml_model")
if _ML_DIR not in sys.path:
    sys.path.insert(0, _ML_DIR)

from model import predict_furniture  

def _model_recommendation(room: "RoomInput") -> dict:
    window_walls = [w.wall for w in room.windows]
    raw = predict_furniture(
        length=room.length,
        breadth=room.width,
        area=room.length * room.width,
        num_windows=len(room.windows),
        setup_type=room.style,
        door_wall=room.doors[0].wall,
        window_walls=window_walls,
    )
    return {
        category: CATEGORY_CODE_TO_NAME.get(category, {}).get(code, code)
        for category, code in raw.items()
    }


def resolve_furniture(room: "RoomInput") -> Tuple[List[str], List[str]]:

    notes: List[str] = []

    user_by_category = {}
    for name in room.required_furniture:
        category = NAME_TO_CATEGORY.get(name)
        if category is None:
            notes.append(f"'{name}' isn't a recognized furniture item; ignored.")
            continue
        user_by_category[category] = name

    if not room.doors:
        notes.append("No door specified; the recommendation model needs one, so using your picks only.")
        return list(user_by_category.values()), notes

    try:
        model_pick = _model_recommendation(room)
    except Exception as e:
        notes.append(f"Recommendation model failed ({e}); using your selections only.")
        model_pick = {}

    final = dict(model_pick)
    final.update(user_by_category)  # user's picks always win, per your instructions

    return list(final.values()), notes
