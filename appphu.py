import streamlit as st
import numpy as np
import subprocess

st.set_page_config(page_title="Dự đoán Đột Quỵ bằng AI", layout="wide")

# =============================
# KHỞI TẠO SESSION STATE
# =============================
if "step" not in st.session_state:
    st.session_state.step = 1

if "history" not in st.session_state:
    st.session_state.history = []

if "symptoms" not in st.session_state:
    st.session_state.symptoms = {}

st.title("🦠 Dự đoán mắc Covid-19")

# =============================
# BƯỚC 1: THÔNG TIN CÁ NHÂN
# =============================
if st.session_state.step == 1:

    st.subheader("1️⃣ Thông tin cá nhân")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        name = st.text_input("Họ và tên")
    with col2:
        age = st.selectbox("Độ tuổi", ["Dưới 18", "18-40", "40-65", "Trên 65"])
    with col3:
        gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
    with col4:
        phone = st.text_input("Số điện thoại")

    address = st.text_input("Địa chỉ")
    job = st.text_input("Nghề nghiệp")

    col_home, col_next = st.columns(2)

    with col_home:
        if st.button("⬅️ Quay về trang chủ", key="home_btn"):
            subprocess.Popen(["streamlit", "run", "main.py"])

    with col_next:
        if st.button("Tiếp ➡", key="next_step1"):
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.gender = gender
            st.session_state.phone = phone
            st.session_state.address = address
            st.session_state.job = job
            st.session_state.step = 2

# =============================
# BƯỚC 2: TRIỆU CHỨNG
# =============================
elif st.session_state.step == 2:

    st.subheader("2️⃣ Triệu chứng thường gặp")
    st.warning("⚠ Các triệu chứng xuất hiện gần đây.")

    symptoms = [
        "Mất thị lực hoặc nhìn mờ",
        "Đau đầu dữ dội bất thường",
        "Chóng mặt",
        "Buồn nôn",
        "giảm ý thức",
        "Đột ngột tê mặt, tay, chân (thường một bên cơ thể)",
        "Méo miệng",
        "Nói ngọng, nói khó"
    ]

    # Khởi tạo nếu chưa có
    for symptom in symptoms:
        if symptom not in st.session_state.symptoms:
            st.session_state.symptoms[symptom] = False

    for symptom in symptoms:
        st.session_state.symptoms[symptom] = st.checkbox(
            symptom,
            value=st.session_state.symptoms[symptom],
            key=f"chk_{symptom}"
        )

    col_back, col_next = st.columns(2)

    with col_back:
        if st.button("⬅ Quay lại", key="back_step2"):
            st.session_state.step = 1

    with col_next:
        if st.button("Tiếp ➡", key="next_step2"):
            symptom_vector = [1 if v else 0 for v in st.session_state.symptoms.values()]
            st.session_state.symptom_vector = symptom_vector
            st.session_state.step = 3

# =============================
# BƯỚC 3: DỰ ĐOÁN
# =============================
elif st.session_state.step == 3:

    st.subheader("3️⃣ Kết quả dự đoán")

    features = np.array([st.session_state.symptom_vector])
    score = np.sum(features)

    if score >= 3:
        result = "🔴 Nguy cơ cao mắc bệnh Đột Quỵ," \
        "Bạn hãy đến cơ sở y tế sớm nhất để bác sĩ kiểm tra và có kế luận chính xác nhẩt."
    else:
        result = "🟢 Nguy cơ thấp mắc bệnh Đột Quỵ," \
        "Bạn vẫn nên kiểm tra và nhận tư vấn từ bác sĩ thường xuyên."

    st.success(result)
    st.session_state.history.append(result)

    col_restart, col_back = st.columns(2)

    with col_restart:
        if st.button("🔄 Làm lại", key="restart_btn"):
            st.session_state.step = 1

    with col_back:
        if st.button("⬅ Quay lại bước 2", key="back_step3"):
            st.session_state.step = 2