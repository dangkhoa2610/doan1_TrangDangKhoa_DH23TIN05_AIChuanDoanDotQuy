import streamlit as st
import numpy as np
import joblib
import os
import subprocess
import pandas as pd

# ========================
# UI CONFIG (PHẢI ĐẶT ĐẦU TIÊN)
# ========================
layout="wide"
st.set_page_config(
    page_title="Stroke AI Predictor",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Stroke Prediction AI")
st.markdown("Ứng dụng dự đoán nguy cơ đột quỵ bằng Machine Learning")

# ========================
# SESSION STATE
# ========================
if "history" not in st.session_state:
    st.session_state.history = []

# ========================
# LOAD MODEL & SCALER
# ========================
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "..", "model", "model.pkl")
scaler_path = os.path.join(current_dir, "..", "model", "scaler.pkl")

if not os.path.exists(model_path) or not os.path.exists(scaler_path):
    st.error("❌ Không tìm thấy model hoặc scaler. Kiểm tra lại thư mục /model/")
    st.stop()

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

columns_path = os.path.join(current_dir, "..", "model", "columns.pkl")
feature_columns = joblib.load(columns_path)

# ========================
# HOME BUTTON
# ========================
if st.button("⬅️ Quay về trang chủ", key="home_btn_app"):
    subprocess.Popen(["streamlit", "run", "main.py"])

st.divider()

# ========================
# INPUT FORM
# ========================
st.subheader("📋 Nhập thông tin sức khỏe")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 👤 Thông tin cá nhân")
    age = st.number_input("Tuổi", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
    married = st.selectbox("Đã kết hôn?", ["Có", "Chưa"])

with col2:
    st.markdown("### ❤️ Tiền sử bệnh lý")
    hypertension = st.selectbox("Tăng huyết áp?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")
    heart_disease = st.selectbox("Bệnh tim?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")
    smoking = st.selectbox("Tình trạng hút thuốc", 
                           ["Không hút", "Đã từng hút", "Hiện đang hút"])

with col3:
    st.markdown("### 📊 Chỉ số cơ thể")
    glucose = st.number_input("Chỉ số đường huyết trung bình (mg/dL)", min_value=0.0, value=100.0)
    bmi = st.number_input("Chỉ số BMI", min_value=0.0, value=22.0)
    residence = st.selectbox("Khu vực sinh sống", ["Thành thị", "Nông thôn"])
    work = st.selectbox("Loại công việc", 
                        ["Tư nhân", "Tự kinh doanh", "Nhà nước"])

st.divider()

# ========================
# ENCODE INPUT
# ========================
input_dict = {
    "age": age,
    "hypertension": hypertension,
    "heart_disease": heart_disease,
    "avg_glucose_level": glucose,
    "bmi": bmi,
    "gender": gender,
    "ever_married": married,
    "work_type": work,
    "residence_type": residence,
    "smoking_status": smoking
}

input_df = pd.DataFrame([input_dict])

# One-hot giống train
input_df = pd.get_dummies(input_df)

# Đảm bảo đủ cột
input_df = input_df.reindex(columns=feature_columns, fill_value=0)

# ========================
# PREDICTION
# ========================
if st.button("🔎 Dự đoán nguy cơ đột quỵ", key="predict_btn"):
    import numpy as np

    # Scale đúng DataFrame đã encode
    input_scaled = scaler.transform(input_df)

# Predict dùng dữ liệu đã scale
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    st.subheader("📊 Kết quả dự đoán")

    percent = probability * 100

    if prediction == 1:
        st.error(f"⚠️ Nguy cơ đột quỵ CAO ({percent:.2f}%)")
    else:
        st.success(f"✅ Nguy cơ đột quỵ THẤP ({percent:.2f}%)")

    st.progress(int(percent))
    st.metric(label="Tỷ lệ nguy cơ", value=f"{percent:.2f}%")

    st.session_state.history.append(f"{percent:.2f}%")