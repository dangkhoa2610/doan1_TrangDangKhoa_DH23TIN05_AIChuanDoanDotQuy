# train.py (FIXED VERSION)

import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

# ==============================
# 1. LOAD DATA
# ==============================
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "..", "data", "healthcare-dataset-stroke-data.csv")
data_path = os.path.abspath(data_path)

data = pd.read_csv(data_path)
data.columns = data.columns.str.strip().str.lower()

# Fix stroke
data['stroke'] = pd.to_numeric(data['stroke'], errors='coerce')
data = data.dropna(subset=['stroke'])
data['stroke'] = data['stroke'].astype(int)

# ==============================
# 2. TIỀN XỬ LÝ
# ==============================

data = data.drop('id', axis=1, errors='ignore')
data['bmi'] = data['bmi'].fillna(data['bmi'].median())

# One-Hot Encoding (KHÔNG drop_first)
data = pd.get_dummies(
    data,
    columns=['gender', 'ever_married', 'work_type', 'residence_type', 'smoking_status'],
    drop_first=False
)

X = data.drop('stroke', axis=1)
y = data['stroke']

# ==============================
# 3. CHIA DATA
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==============================
# 4. SMOTE
# ==============================
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# ==============================
# 5. SCALE DATA
# ==============================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ==============================
# 6. TRAIN MODEL
# ==============================
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ==============================
# 7. LƯU MODEL
# ==============================
model_dir = os.path.join(current_dir, "..", "model")
os.makedirs(model_dir, exist_ok=True)

joblib.dump(model, os.path.join(model_dir, "model.pkl"))
joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))
joblib.dump(X.columns.tolist(), os.path.join(model_dir, "columns.pkl"))

print("Đã train và lưu model thành công!")