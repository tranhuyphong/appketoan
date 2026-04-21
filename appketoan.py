import streamlit as st
import random
import datetime
from supabase import create_client

# ================= SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= INIT STATE =================
def init_state():
    defaults = {
        "user": None,
        "coins": 100,
        "streak": 0,
        "last_login": "",
        "percent": None,
        "q_index": 0,
        "chat_history": [],
        "skills": {},
        "learned_lessons": [],
        "daily_learn": 0,
        "performance": 100
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ================= DATA PERSISTENCE =================
def save_progress():
    if st.session_state.user:
        try:
            supabase.table("users").upsert({
                "email": st.session_state.user,
                "coins": st.session_state.coins,
                "streak": st.session_state.streak,
                "learned_lessons": st.session_state.learned_lessons,
                "daily_learn": st.session_state.daily_learn,
                "performance": st.session_state.performance,
                "last_login": st.session_state.last_login
            }).execute()
        except Exception as e:
            print(f"Lỗi lưu data: {e}")

# ================= LOGIN / REGISTER =================
if st.session_state.user is None:
    st.title("🚀 PHONG AI ACCOUNTING")
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký tài khoản"])

    with tab1:
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_pw")
        
        if st.button("Đăng nhập"):
            try:
                res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                if res.user:
                    st.session_state.user = res.user.email
                    
                    # TẢI DỮ LIỆU CŨ TỪ DATABASE
                    data = supabase.table("users").select("*").eq("email", res.user.email).execute()
                    if data.data:
                        u = data.data[0]
                        st.session_state.coins = u.get("coins", 100)
                        st.session_state.streak = u.get("streak", 0)
                        st.session_state.learned_lessons = u.get("learned_lessons", [])
                        st.session_state.last_login = u.get("last_login", "")
                        st.session_state.performance = u.get("performance", 100)
                    
                    st.success("Đăng nhập thành công!")
                    st.rerun()
            except:
                st.error("Sai tài khoản hoặc mật khẩu!")
    
    with tab2:
        reg_email = st.text_input("Email đăng ký")
        reg_password = st.text_input("Password đăng ký", type="password")
        if st.button("Thực hiện Đăng ký"):
            try:
                supabase.auth.sign_up({"email": reg_email, "password": reg_password})
                st.success("Đăng ký thành công! Hãy chuyển qua tab Đăng nhập.")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    st.stop()

# ================= DAILY BONUS =================
today = str(datetime.date.today())
if st.session_state.last_login != today:
    st.session_state.coins += 20
    st.session_state.last_login = today
    st.success("🎁 Quà đăng nhập ngày mới +20 coins")
    save_progress()

if st.session_state.daily_learn >= 3:
    st.success("🎁 Chăm chỉ học tập +30 coins")
    st.session_state.coins += 30
    st.session_state.daily_learn = 0
    save_progress()

# ================= IMPORT MODULES =================
# (Giữ nguyên các dòng import của bạn)
from data.career_tasks import career_tasks
from data.learning_path import learning_path
from data.question_bank import question_bank
from engine.ai_teacher import teacher_explain
from engine.progress_tracker import update_progress
from engine.classroom_ai import classroom_chat
from data.curriculum import curriculum
from data.dictionary import dictionary
from data.jobs import jobs
from engine.boss_ai import boss_msg
from engine.ai_grader import grade
from data.case_study import case_studies

# ================= UI HEADER =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")
coins = st.session_state.coins

if coins < 100: rank = "🥉 Intern"
elif coins < 300: rank = "🥈 Junior"
elif coins < 600: rank = "🥇 Senior"
else: rank = "👑 Manager"

st.markdown(f"<div style='padding:20px;background:#1e293b;border-radius:20px'><h2>📱 Phong AI Accounting</h2>💰 {coins} | 🔥 {st.session_state.streak} | 🎖 {rank}</div>", unsafe_allow_html=True)

# ================= MENU =================
menu = st.sidebar.radio("Menu", ["📘 Học", "🎓 Lớp học AI (Quiz)", "🎓 Lớp học AI (Chat)", "💼 Đi làm", "🧾 Case Study", "📊 Dashboard", "📚 Từ điển"])

# ================= HỌC =================
if menu == "📘 Học":
    st.header("📘 Lộ trình học kế toán")
    total = sum(len(m["lessons"]) for l in learning_path for m in l["modules"])
    done = len(st.session_state.learned_lessons)
    st.progress(done / total if total > 0 else 0)
    st.write(f"📊 Tiến độ: {done}/{total}")

    for i, lvl in enumerate(learning_path):
        is_unlocked = coins >= i * 300
        with st.expander(f"{'✅' if is_unlocked else '🔒'} {lvl['level']}"):
            for module in lvl["modules"]:
                st.write(f"--- **{module['name']}** ---")
                for lesson in module["lessons"]:
                    learned = lesson in st.session_state.learned_lessons
                    c1, c2 = st.columns([4,1])
                    c1.write(f"{'✅' if learned else '📖'} {lesson}")
                    if is_unlocked and not learned:
                        if c2.button("Học", key=lesson):
                            st.session_state.learned_lessons.append(lesson)
                            reward = random.randint(5, 15)
                            st.session_state.coins += reward
                            st.session_state.daily_learn += 1
                            save_progress()
                            st.rerun()

# ================= CÁC MENU KHÁC =================
# (Bạn chỉ cần copy lại logic Quiz, Chat, Đi làm... của bạn vào đây)
# LƯU Ý: Ở cuối mỗi hành động cộng coin, hãy dùng save_progress() thay vì save_coins()

elif menu == "🎓 Lớp học AI (Quiz)":
    q = question_bank[st.session_state.q_index]
    st.subheader(q["question"])
    answer = st.radio("Chọn:", q["options"])
    if st.button("Nộp bài"):
        if q["options"].index(answer) == q["correct"]:
            st.session_state.streak += 1
            st.session_state.coins += 20
            st.success("Chính xác!")
        else:
            st.session_state.streak = 0
            st.error("Sai rồi!")
        save_progress()
    if st.button("Câu tiếp"):
        st.session_state.q_index = (st.session_state.q_index + 1) % len(question_bank)
        st.rerun()

elif menu == "📊 Dashboard":
    st.metric("Tổng Coin", st.session_state.coins)
    st.write("Các bài đã hoàn thành:")
    for lesson in st.session_state.learned_lessons:
        st.write(f"- {lesson}")

elif menu == "📚 Từ điển":
    key = st.text_input("Nhập mã tài khoản (Ví dụ: 111)")
    if key in dictionary:
        st.success(dictionary[key])
