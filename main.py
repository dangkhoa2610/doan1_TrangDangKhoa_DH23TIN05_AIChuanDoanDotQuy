import streamlit as st
import subprocess
import sys
import os

st.set_page_config(page_title="Ciel_AI", page_icon="🧠", layout="centered")

st.title("🧠 Ciel_AI - Stroke Prediction System")
st.markdown("### Hệ thống Chuẩn đoán nguy cơ đột quỵ")

st.divider()

# Khởi tạo session lưu lịch sử nếu chưa có
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Chọn chức năng:")

col1, col2 = st.columns(2)

# Lấy đường dẫn file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(BASE_DIR, "app.py")
appphu_path = os.path.join(BASE_DIR, "appphu.py")

with col1:
    if st.button("🧠 Dự đoán triệu chứng"):
        subprocess.Popen(["streamlit", "run", appphu_path])

with col2:
    if st.button("📊 Dự đoán chỉ số cơ thể"):
        subprocess.Popen(["streamlit", "run", app_path])


#them
st.divider()
st.subheader("📁 Lịch sử chuẩn đoán")

if len(st.session_state.history) == 0:
    st.info("Chưa có dữ liệu chuẩn đoán nào.")
else:
    for i, record in enumerate(st.session_state.history, 1):
        st.write(f"Lần {i}: {record}")

st.divider()
st.subheader("📊 Biểu đồ tỷ lệ mắc bệnh")

if len(st.session_state.history) > 0:
    # Đếm số mắc và không mắc
    stroke_count = sum(1 for r in st.session_state.history if "Nguy cơ cao" in r)
    no_stroke_count = len(st.session_state.history) - stroke_count

    import pandas as pd

    data = pd.DataFrame({
        "Kết quả": ["Nguy cơ cao", "Nguy cơ thấp"],
        "Số lượng": [stroke_count, no_stroke_count]
    })

    st.bar_chart(data.set_index("Kết quả"))
else:
    st.info("Chưa có dữ liệu để vẽ biểu đồ.")