"""
Retrains the Decora furniture-recommendation model on
interior_design_dataset_bedroom.csv

Key differences from the old dataset / old script:
  - Furniture columns (bed, table, chair, ...) are TYPE CODES, not 0/1 flags.
    NaN means "this item isn't placed in the room" -> encoded as 'none'.
  - 'dustbin' only ever has one value in this data -> nothing to learn,
    so it's dropped from training and hardcoded back at prediction time.
  - window_wall_1 / window_wall_2 are unordered slots (a single window can
    land in either column), so they're converted into 4 stable binary flags
    (window_north/south/east/west) instead of being encoded as-is.
  - Added an actual train/test evaluation (the old script imported
    train_test_split but never called it).
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score
import joblib

# ---- Load dataset ----
# Use a path relative to this script so it runs on any machine.
df = pd.read_csv(r'E:\Second Sem Project\Main Decora Code\datasets\interior_design_dataset_bedroom.csv')

print("Columns in dataset:", list(df.columns))
print("Total rows:", len(df))

# ---- Feature engineering ----
# Collapse the two ambiguous window-wall slots into 4 stable per-wall flags.
for wall in ['north', 'south', 'east', 'west']:
    df[f'window_{wall}'] = (
        (df['window_wall_1'] == wall) | (df['window_wall_2'] == wall)
    ).astype(int)

numeric_features = ['room_length_ft', 'room_breadth_ft', 'room_area_sqft', 'num_windows',
                     'window_north', 'window_south', 'window_east', 'window_west']
categorical_features = ['room_setup_type', 'door_wall']

# ---- Targets ----
all_furniture_cols = ['bed', 'table', 'chair', 'wardrobe', 'bookshelf',
                       'bedsidetable', 'dresser', 'dustbin', 'mirror']

target_cols = []
constant_targets = {}   # columns with only 1 unique value (incl. presence/absence) -> not modeled, hardcoded
for col in all_furniture_cols:
    # IMPORTANT: check uniqueness *after* treating missing as its own 'none'
    # category, so an item that's sometimes absent (NaN) and sometimes one
    # fixed type (e.g. bedsidetable: NaN or 'bt') is NOT mistaken for constant.
    vals = df[col].fillna('none').unique()
    if len(vals) <= 1:
        constant_targets[col] = vals[0] if len(vals) else None
        continue
    target_cols.append(col)

print("\nTargets to model:", target_cols)
print("Constant targets (hardcoded, not modeled):", constant_targets)

df[target_cols] = df[target_cols].fillna('none')

# ---- Encode features ----
feature_encoders = {}
X = pd.DataFrame(index=df.index)
for col in numeric_features:
    X[col] = df[col]

for col in categorical_features:
    le = LabelEncoder()
    X[f'{col}_enc'] = le.fit_transform(df[col])
    feature_encoders[f'le_{col}'] = le

feature_order = numeric_features + [f'{c}_enc' for c in categorical_features]
X = X[feature_order]

print("\nTraining with", X.shape[1], "features:", feature_order)

# ---- Encode targets ----
target_encoders = {}
Y = pd.DataFrame(index=df.index)
for col in target_cols:
    le = LabelEncoder()
    Y[col] = le.fit_transform(df[col])
    target_encoders[col] = le

# ---- Train / evaluate ----
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = MultiOutputClassifier(
    RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
    n_jobs=-1
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nHeld-out accuracy per item:")
for i, col in enumerate(target_cols):
    acc = accuracy_score(y_test[col], y_pred[:, i])
    print(f"  {col:15s}: {acc:.3f}")

# ---- Refit on full dataset for the saved/deployed model ----
model.fit(X, Y)

joblib.dump(model, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decora_model.pkl'))
joblib.dump(
    {
        'feature_order': feature_order,
        'le_room_setup_type': feature_encoders['le_room_setup_type'],
        'le_door_wall': feature_encoders['le_door_wall'],
        'target_cols': target_cols,
        'target_encoders': target_encoders,
        'constant_targets': constant_targets,
    },
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decora_encoders.pkl')
)

print("\nModel retrained successfully.")
print("Files saved: decora_model.pkl, decora_encoders.pkl")
