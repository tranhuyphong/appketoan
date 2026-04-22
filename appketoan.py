import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

# ================= 1. CẤU HÌNH TRANG =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= 2. IMPORT DỮ LIỆU & ENGINE =================
try:
    from data.career_tasks import career_tasks
    from data.curriculum import curriculum
    from data.question_bank import question_bank
    from data.dictionary import dictionary
    from data.case_study import case_studies
    from engine.ai_teacher import teacher_explain
    from engine.progress_tracker import update_progress
    from engine.classroom_ai import classroom_chat
    from engine.boss_ai import boss_msg
    from engine.ai_grader import grade
    from engine.financial_report import generate_report
    from engine.fraud_detection import detect_fraud
    from data.finance_data import transactions
except ImportError as e:
    st.error(f"⚠️ Thiếu file hệ thống: {e}")
    curriculum = curriculum if 'curriculum' in locals() else []
    question_bank = question_bank if 'question_bank' in locals() else []

# ================= 3. KẾT NỐI SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= 4. RENDER MAP (ZIGZAG & CLICK) =================
def render_duolingo_pro(unit_id, lessons):
    html = f"""
    <style>
    .map {{ display: flex; flex-direction: column; align-items: center; gap: 35px; padding: 20px; }}
    .row {{ width: 100%; display: flex; }}
    .left {{ justify-content: flex-start; padding-left: 20%; }}
    .right {{ justify-content: flex-end; padding-right: 20%; }}
    .node {{ 
        width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; 
        justify-content: center; font-weight: bold; font-size: 22px; color: white; 
        cursor: pointer; transition: all 0.25s ease; 
    }}
    .node:hover {{ transform: scale(1.15); }}
    .done {{ background: #22c55e; }}
    .current {{ background: #3b82f6; box-shadow: 0 0 20px #3b82f6; animation: pulse 1.5s infinite; }}
    .locked {{ background: #334155; opacity: 0.4; cursor: not-allowed; }}
    .boss {{ background: gold; color: black; box-shadow: 0 0 15px gold; }}
    @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
    .line {{ width: 6px; height: 40px; background: #475569; }}
    </style>
    <div class="map">
    """
    for i, lesson in enumerate(lessons):
        status = lesson["status"]
        cls = f"node {status}"
        if lesson.get("type") == "boss": cls += " boss"
        
        side = "left" if i % 2 == 0 else "right"
        label = lesson.get("label", str(i+1))
        # JavaScript để gửi message về Streamlit
        click_js = f"window.parent.postMessage('{unit_id}|{i}', '*')" if status != "locked" else ""

        html += f"""
        <div class="row {side}">
            <div class="{cls}" onclick="{click_js}">{label}</div>
        </div>
        """
        if i < len(lessons) - 1: html += "<div class='line'></div>"
    html += "</div>"

    return components.html(f"""
    {html}
    <script>
    window.addEventListener("message", (event) => {{
        const data = event.data;
        if (data && typeof data === 'string' && data.includes('|')) {{
            window.parent.postMessage({{ type: "streamlit:setComponentValue", value: data }}, "*");
        }}
    }});
    </script>
    """, height=650)

# ================= 5. HÀM HỖ TRỢ =================
def load_progress():
    try:
        res = supabase.table("users_progress").select("*").eq("email", st.session_state.user).execute()
        return {r["lesson_id"]: r for r in res.data}
    except: return {}

def save_coins():
    if "user" in st.session_state:
        try:
            supabase.table("users").upsert({"email": st.session_state.user, "coins": st.session_state.coins}).execute()
        except: pass

# ================= 6. SESSION STATE =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins": 100, "streak": 0, "last_login": "", "lesson_progress": {},
        "current_lesson": None, "q_index": 0, "chat_history": []
    })

# ================= 7. ĐĂNG NHẬP (LƯU Ý: ĐÃ SỬA ĐỂ CHẠY ỔN ĐỊNH) =================
if "user" not in st.session_state:
    st.title("🚀 PHONG AI ACCOUNTING")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    if st.button("Đăng nhập"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": pw})
            if res.user:
                st.session_state.user = res.user.email
                st.rerun()
        except: st.error("Lỗi đăng nhập!")
    st.stop()

# ================= 8. GIAO DIỆN CHÍNH =================
coins = st.session_state.coins
rank = "🥉 Intern" if coins < 100 else "🥈 Junior" if coins < 300 else "🥇 Senior" if coins < 600 else "👑 Manager"

st.sidebar.markdown(f"### 🎖️ Rank: {rank}")
st.sidebar.markdown(f"### 💰 Coins: {coins}")

menu = st.sidebar.radio("Menu", [
    "📘 Học", "🎓 Lớp học AI (Quiz)", "🎓 Lớp học AI (Chat)",
    "💼 Đi làm", "🧾 Case Study", "📊 Dashboard", "🏆 Leaderboard"
])

# ================= 9. LOGIC CÁC MENU (QUAN TRỌNG ĐỂ HẾT MÀN HÌNH ĐEN) =================

if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    # Hiển thị nội dung bài học khi click vào Node
    if st.session_state.get("current_lesson"):
        lesson = st.session_state.current_lesson
        with st.container(border=True):
            st.markdown(f"## 📖 {lesson['title']}")
            st.write(lesson["content"])
            if st.button("❌ Đóng"):
                st.session_state.current_lesson = None
                st.rerun()
        st.divider()

    for level in curriculum:
        # SỬA LỖI KeyError: dùng .get() để an toàn
        level_name = level.get('level', level.get('name', 'Cấp độ mới'))
        required = level.get("unlock_coins", 0)
        unlocked = st.session_state.coins >= required

        st.markdown(f"## {'🔓' if unlocked else '🔒'} {level_name} (Cần {required} 💰)")

        if unlocked:
            for module in level.get("modules", []):
                st.markdown(f"### 📚 {module['name']}")
                
                # Tính toán trạng thái các Node
                lesson_nodes = []
                prev_passed = True
                for i, lesson in enumerate(module["lessons"]):
                    l_id = f"{level_name}_{module['name']}_{lesson['title']}"
                    prog = st.session_state.lesson_progress.get(l_id, {"submitted": False, "score": 0})
                    
                    status = "done" if prog["submitted"] and prog["score"] >= 70 else "current" if prev_passed else "locked"
                    lesson_nodes.append({"status": status, "type": "lesson", "label": str(i+1)})
                    prev_passed = (status == "done")

                # Node Boss cuối Module
                lesson_nodes.append({"status": "current" if prev_passed else "locked", "type": "boss", "label": "👑"})

                # Gọi hàm Render và nhận giá trị click
                clicked = render_duolingo_pro(module["name"], lesson_nodes)

                if clicked:
                    unit, index = clicked.split("|")
                    idx = int(index)
                    if unit == module["name"] and idx < len(module["lessons"]):
                        st.session_state.current_lesson = module["lessons"][idx]
                        st.rerun()

elif menu == "🎓 Lớp học AI (Quiz)":
    st.header("🎓 Trắc nghiệm Kế toán")
    st.info("Tính năng đang được cập nhật dữ liệu...")

elif menu == "🎓 Lớp học AI (Chat)":
    st.header("💬 Chat với Giảng viên AI")
    # Thêm logic chat cơ bản ở đây
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input("Hỏi về định khoản..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.rerun()

elif menu == "💼 Đi làm":
    st.header("🏢 Career Mode")
    st.write("Giải quyết các tình huống thực tế tại doanh nghiệp.")

elif menu == "📊 Dashboard":
    st.header("📊 Tiến độ của bạn")
    st.metric("Tổng xu tích lũy", st.session_state.coins)

elif menu == "🏆 Leaderboard":
    st.header("🏆 Bảng xếp hạng cao thủ")
    st.write("Ai là kế toán trưởng giỏi nhất?")

# ================= 10. ĐĂNG XUẤT =================
st.sidebar.divider()
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
