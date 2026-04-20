import streamlit as st
from data import ACADEMY_DATA

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(page_title="Học Viện Kế Toán Slay", layout="wide")

if "lesson_idx" not in st.session_state: st.session_state.lesson_idx = 0
if "quiz_passed" not in st.session_state: st.session_state.quiz_passed = False

# --- SIDEBAR NAV ---
with st.sidebar:
    st.title("💅 Kế Toán Slay")
    phase_id = st.selectbox("Chọn Chặng:", list(ACADEMY_DATA.keys()), format_func=lambda x: ACADEMY_DATA[x]["name"])
    
    modules = ACADEMY_DATA[phase_id]["modules"]
    mod_id = st.radio("Học phần:", list(modules.keys()), format_func=lambda x: f"{'🔒' if modules[x]['is_premium'] else '📖'} {modules[x]['name']}")
    
    # Kiểm tra nếu đổi Module thì reset bài học
    if "last_mod" not in st.session_state or st.session_state.last_mod != mod_id:
        st.session_state.lesson_idx = 0
        st.session_state.last_mod = mod_id
        st.session_state.quiz_passed = False

# --- HIỂN THỊ NỘI DUNG ---
module = ACADEMY_DATA[phase_id]["modules"][mod_id]
lessons = module["lessons"]

if not lessons:
    st.info("🚧 Nội dung đang được cập nhật...")
else:
    lesson = lessons[st.session_state.lesson_idx]
    
    st.title(f"Bài {st.session_state.lesson_idx + 1}: {lesson['title']}")
    
    tab_learn, tab_quiz = st.tabs(["📚 Bài Giảng Trực Quan", "✍️ Kiểm Tra Đầu Ra"])
    
    with tab_learn:
        st.markdown(f"#### 📖 Lý thuyết cốt lõi\n{lesson['theory']}")
        
        # Chèn Hình ảnh / Sơ đồ tư duy
        if "visuals" in lesson:
            st.write("---")
            st.subheader("🧠 Sơ đồ tư duy & Trực quan")
            for img in lesson["visuals"]:
                st.write(img) # Streamlit sẽ hiển thị tag [Image of...]
        
        # Phần kiến thức mở rộng
        with st.expander("🚀 Kiến thức mở rộng (Deep Dive)"):
            st.success(lesson.get("deep_dive", "Đang cập nhật..."))

    with tab_quiz:
        st.subheader("🔥 Vượt qua thử thách để đi tiếp")
        correct_needed = len(lesson["exercises"])
        score = 0
        
        for i, ex in enumerate(lesson["exercises"]):
            st.write(f"**Câu {i+1}:** {ex['q']}")
            ans = st.radio(f"Chọn đáp án (Câu {i+1}):", ex['options'], key=f"q_{mod_id}_{st.session_state.lesson_idx}_{i}")
            if ans == ex['correct']:
                score += 1
        
        # Kiểm tra điều kiện qua bài
        if score == correct_needed:
            st.session_state.quiz_passed = True
            st.balloons()
            st.success("✅ Tuyệt vời! Bạn đã nắm vững kiến thức bài này.")
        else:
            st.session_state.quiz_passed = False
            st.warning(f"⚡ Bạn cần đúng {score}/{correct_needed} câu. Hãy đọc lại phần Deep Dive nhé!")

    # --- NAVIGATION ---
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.lesson_idx > 0:
            if st.button("⬅️ Quay lại"):
                st.session_state.lesson_idx -= 1
                st.session_state.quiz_passed = False
                st.rerun()
                
    with col2:
        if st.session_state.lesson_idx < len(lessons) - 1:
            if st.session_state.quiz_passed:
                if st.button("Bài tiếp theo ➡️", type="primary"):
                    st.session_state.lesson_idx += 1
                    st.session_state.quiz_passed = False
                    st.rerun()
            else:
                st.button("🔒 Hoàn thành kiểm tra để tiếp tục", disabled=True)
