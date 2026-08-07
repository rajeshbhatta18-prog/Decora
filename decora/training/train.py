import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "data", "decora_bedroom_dataset_v2.csv")
df = pd.read_csv(CSV_PATH)

print("Columns in dataset:", list(df.columns))
print("Total rows:", len(df))

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
    vals = df[col].fillna('none').unique()
    if len(vals) <= 1:
        constant_targets[col] = vals[0] if len(vals) else None
        continue
    target_cols.append(col)

print("\nTargets to model:", target_cols)
print("Constant targets (Prefixed furniture):", constant_targets)

df[target_cols] = df[target_cols].fillna('none')

# Encode features 
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

# Encode targets 
target_encoders = {}
Y = pd.DataFrame(index=df.index)
for col in target_cols:
    le = LabelEncoder()
    Y[col] = le.fit_transform(df[col])
    target_encoders[col] = le

# Train / evaluate 

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=45)

model = MultiOutputClassifier(
    RandomForestClassifier(n_estimators=200, max_depth=10, random_state=45, n_jobs=-1),
    n_jobs=-1
)

model.fit(X_train, y_train)
train_pred = model.predict(X_train)
print(f"\nTraining accuracy {train_pred}")

y_pred = model.predict(X_test)
sum_accuracy = 0
print("\nHeld-out accuracy per item:")
for i, col in enumerate(target_cols):
    acc = accuracy_score(y_test[col], y_pred[:, i])
    sum_accuracy += acc
    print(f"  {col:15s}: {acc:.3f} ")
overall_accuracy = sum_accuracy / len(target_cols) if target_cols else 0
print(f"\nOverall accuracy: {overall_accuracy:.3f}")

# Refit on full dataset for the saved/deployed model 
model.fit(X, Y)

ML_MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "ml_model")
joblib.dump(model, os.path.join(ML_MODEL_DIR, 'decora_model.pkl'))
joblib.dump(
    {
        'feature_order': feature_order,
        'le_room_setup_type': feature_encoders['le_room_setup_type'],
        'le_door_wall': feature_encoders['le_door_wall'],
        'target_cols': target_cols,
        'target_encoders': target_encoders,
        'constant_targets': constant_targets,
    },
    os.path.join(ML_MODEL_DIR, 'decora_encoders.pkl')
)

print("\nModel retrained successfully.")
print(f"Files saved to: {ML_MODEL_DIR}")
# train_pred = model.predict(X_train)

# # Calculate testing accuracy
# test_pred = model.predict(X_test)

# # Calculate F1 score
# micro_f1 = f1_score(y_test, test_pred, average="micro")
# # Retrain the model using the full dataset

# model.fit(X, Y)
# # Save the trained model

# joblib.dump(...)


# # Save encoders

# joblib.dump(...)


# # Display final results

# print(...)
