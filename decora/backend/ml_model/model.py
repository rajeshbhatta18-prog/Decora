
import os
import pandas as pd
import joblib

_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(_DIR, 'decora_model.pkl'))
enc = joblib.load(os.path.join(_DIR, 'decora_encoders.pkl'))


def predict_furniture(length, breadth, area, num_windows, setup_type, door_wall, window_walls):
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
        length= 13.0,
        breadth= 12.0,
        area= 100.0,
        num_windows= 2,
        setup_type= 'luxury',
        door_wall='north',
        window_walls= ['south', 'east'],
    )
    def print_furniture():
        print("Predicted furniture:", furniture)
        return furniture
    print_furniture()
