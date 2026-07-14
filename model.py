"""
Loads the trained Decora model and predicts furniture for a given room.

Fixes vs. the old Model.py:
  - Uses the real category names for this dataset: door_wall / windows are
    compass directions (north/south/east/west), not 'top'/'bottom'.
  - Windows are given as a list of walls instead of a single 'window_wall',
    since a room can have windows on 1 or 2 walls.
  - Feature order is read from the saved encoders bundle (feature_order)
    instead of being hand-typed, so Model.py can never drift out of sync
    with what retrain.py actually trained on.
  - Output includes the predicted TYPE of each item (e.g. bed -> 'db'),
    and only includes optional items the model predicts are present
    (i.e. not predicted as 'none').
"""
import os
import numpy as np
import pandas as pd
import joblib

_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(_DIR, 'decora_model.pkl'))
enc = joblib.load(os.path.join(_DIR, 'decora_encoders.pkl'))


def predict_furniture(length, breadth, area, num_windows, setup_type, door_wall, window_walls):
    """
    length, breadth, area : room dimensions (ft / sqft)
    num_windows           : 1 or 2
    setup_type            : 'budget' | 'standard' | 'luxury'
    door_wall             : 'north' | 'south' | 'east' | 'west'
    window_walls          : list of `num_windows` compass directions,
                             e.g. ['north'] or ['north', 'east']
    """
    if len(window_walls) != num_windows:
        raise ValueError(f"num_windows={num_windows} but got {len(window_walls)} window_walls")

    window_flags = {f'window_{w}': int(w in window_walls) for w in ['north', 'south', 'east', 'west']}

    setup_enc = enc['le_room_setup_type'].transform([setup_type])[0]
    door_enc = enc['le_door_wall'].transform([door_wall])[0]

    row = {
        'room_length_ft': length,
        'room_breadth_ft': breadth,
        'room_area_sqft': area,
        'num_windows': num_windows,
        'window_north': window_flags['window_north'],
        'window_south': window_flags['window_south'],
        'window_east': window_flags['window_east'],
        'window_west': window_flags['window_west'],
        'room_setup_type_enc': setup_enc,
        'door_wall_enc': door_enc,
    }

    # Build the feature vector in the exact order the model was trained on.
    input_data = pd.DataFrame([[row[c] for c in enc['feature_order']]], columns=enc['feature_order'])

    pred = model.predict(input_data)[0]

    result = {}
    for i, col in enumerate(enc['target_cols']):
        val = enc['target_encoders'][col].inverse_transform([pred[i]])[0]
        if val != 'none':
            result[col] = val

    # Add back items that were constant in the training data (e.g. dustbin).
    for col, val in enc['constant_targets'].items():
        if val is not None:
            result[col] = val

    return result


if __name__ == '__main__':
    furniture = predict_furniture(
        length=10.0,
        breadth=10.0,
        area=100.0,
        num_windows=2,
        setup_type='standard',
        door_wall='north',
        window_walls=['south', 'east'],
    )
    print("Predicted furniture:", furniture)
