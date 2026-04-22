import streamlit as st
import random
import datetime
from supabase import create_client

# ================= IMPORT DATA & ENGINE =================
# Đảm bảo các file này tồn tại trong thư mục data/ và engine/
try:
    from data.career_tasks import career_tasks
    from data.learning_path import learning_path
    from data.question_bank import question_bank
    from engine.ai_teacher import teacher_explain
    from engine.progress_tracker import update_progress
    from engine.classroom_ai import classroom_chat
    from data.curriculum import curriculum
    from data.dictionary import dictionary
    # from data.jobs import jobs # Mở ra nếu có file này
    from engine.boss_ai import boss_msg
    from engine.ai_grader import grade
    from data.case_study import case_studies
except ImportError as e:
    st.error(f"Thiếu file dữ liệu: {e}")

# ================= SUPABASE CONFIG =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indqd3Rvd21kY2RrcHJ5eGNxcXR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3NjY1NDMsImV4cCI6MjA5MjM0MjU0M30.jX4wAiXNezvmnwvr1hucjRxANZ5jWgzwn_9BsVCoueg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= INIT STATE =================
def init_state():
    defaults = {
        "coins": 100,
        "streak": 0,
        "last_login": "",
        "percent": None,
        "q_index": 0,
        "chat_history": [],
        "skills": {},
        "learned_lessons": [],
        "daily_learn": 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ================= HELPER FUNCTIONS =================
def save_coins():
    if "user" in st.session_state and st.session_state.user:
        try:
            supabase.table("users").upsert({
                "email": st.session_state.user,
                "coins": st.session_state.coins
            }).execute()
        except Exception as e:
            print(f"Lưu coin thất bại: {e}")

def save_progress(lesson_id, score):
    try:
        supabase.table("users_progress").upsert({
            "email": st.session_state.user,
            "lesson_id": lesson_id,
            "status": "done",
            "score": score,
            "last_learned": str(datetime.date.today())
        }).execute()
    except Exception as e:
        print("Save progress error:", e)

def load_progress():
    try:
        res = supabase.table("users_progress").select("*").eq("email", st.session_state.user).execute()
        return {r["lesson_id"]: r for r in res.data}
    except:
        return {}

# ================= LOGIN / REGISTER =================
if "user" not in st.session_state:
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
                    st.success("Đăng nhập thành công!")
                    st.rerun()
            except:
                st.error("Sai tài khoản hoặc mật khẩu!")
    
    with tab2:
        reg_email = st.text_input("Email đăng ký", key="reg_email")
        reg_password = st.text_input("Password đăng ký", type="password", key="reg_pw")
        confirm_password = st.text_input("Xác nhận Password", type="password", key="reg_pw_conf")
        if st.button("Thực hiện Đăng ký"):
            if reg_password != confirm_password:
                st.warning("Mật khẩu xác nhận không khớp!")
            else:
                try:
                    supabase.auth.sign_up({"email": reg_email, "password": reg_password})
                    st.success("Tạo thành công! Hãy đăng nhập.")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
    st.stop()

# ================= DAILY REWARDS =================
today = str(datetime.date.today())
if st.session_state.last_login != today:
    st.session_state.coins += 20
    st.session_state.last_login = today
    st.success("🎁 Daily +20 coins")
    save_coins()

if st.session_state.daily_learn >= 3:
    st.success("🎁 Daily học đủ 3 bài +30 coins")
    st.session_state.coins += 30
    st.session_state.daily_learn = 0
    save_coins()

# ================= UI HEADER =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")
coins = st.session_state.coins
rank = "🥉 Intern"
if coins >= 600: rank = "👑 Manager"
elif coins >= 300: rank = "🥇 Senior"
elif coins >= 200: rank = "🥈 Junior"

st.markdown(f"<div style='padding:20px;background:#1e293b;border-radius:20px'><h2>📱 Phong AI Accounting</h2>💰 {coins} | 🔥 {st.session_state.streak} | 🎖 {rank}</div>", unsafe_allow_html=True)

# ================= MENU =================
menu = st.sidebar.radio("Menu", [
    "📘 Học", "🎓 Lớp học AI (Quiz)", "🎓 Lớp học AI (Chat)", 
    "💼 Đi làm", "🧾 Case Study", "📊 Dashboard", 
    "📊 Financial Report", "🤖 Chấm bút toán", "📚 Từ điển", 
    "🚨 Fraud Detection", "🏆 Leaderboard"
])

# ================= XỬ LÝ MENU =================
if menu == "📘 Học":
    st.header("📘 Lộ trình học")
    progress_data = load_progress()

    for level in learning_path:
        if st.session_state.coins < level.get("unlock_coins", 0):
            st.warning(f"🔒 Mở khóa khi đạt {level['unlock_coins']} coins")
            continue

        st.subheader(f"🔥 {level['level']}")
        for module in level["modules"]:
            st.markdown(f"### 📚 {module['name']}")
            total = len(module["lessons"])
            done = sum(1 for l in module["lessons"] if l["id"] in progress_data)
            st.progress(done / total)

            for lesson in module["lessons"]:
                lesson_key = f"lesson_{lesson['id']}"
                if lesson_key not in st.session_state:
                    st.session_state[lesson_key] = {"submitted": False, "score": 0}
                
                lesson_state = st.session_state[lesson_key]
                is_done = lesson["id"] in progress_data

                with st.expander(f"{'✅' if is_done else '📖'} {lesson['title']}"):
                    st.write(lesson["content"])
                    st.divider()
                    st.write("🧠 Bài kiểm tra")
                    
                    correct_count = 0
                    for i, q in enumerate(lesson["quiz"]):
                        ans = st.radio(q["question"], q["options"], key=f"{lesson['id']}_{i}", disabled=lesson_state["submitted"])
                        if ans == q["options"][q["answer"]]:
                            correct_count += 1
                    
                    if not lesson_state["submitted"]:
                        if st.button("🚀 Nộp bài", key=f"btn_{lesson['id']}"):
                            score = int((correct_count / len(lesson["quiz"])) * 100)
                            lesson_state["submitted"] = True
                            lesson_state["score"] = score
                            if score >= 70:
                                st.success(f"🎉 Pass {score}%")
                                save_progress(lesson["id"], score)
                                if lesson["id"] not in st.session_state.learned_lessons:
                                    st.session_state.learned_lessons.append(lesson["id"])
                                    st.session_state.coins += lesson.get("xp", 20)
                                    st.session_state.daily_learn += 1
                            else:
                                st.error(f"❌ Fail {score}% (Cần ≥ 70%)")
                            save_coins()
                            st.rerun()
                    else:
                        st.info(f"Kết quả: {lesson_state['score']}%")

elif menu == "🎓 Lớp học AI (Quiz)":
    # (Code phần Quiz giữ nguyên nhưng đảm bảo thụt đầu dòng đúng)
    q = question_bank[st.session_state.q_index]
    st.subheader(q["question"])
    answer = st.radio("Chọn:", q["options"])
    if st.button("Nộp bài"):
        correct = q["options"].index(answer) == q["correct"]
        update_progress(q["skill"], correct, st.session_state)
        if correct:
            st.session_state.streak += 1
            reward = min(10 + st.session_state.streak * 2, 30)
            st.success(f"✅ +{reward} coins")
            st.session_state.coins += reward
        else:
            st.session_state.streak = 0
            st.error("❌ Sai rồi!")
        st.info(q["explain"])
        save_coins()
    if st.button("➡️ Câu tiếp"):
        st.session_state.q_index = (st.session_state.q_index + 1) % len(question_bank)
        st.rerun()

elif menu == "📊 Dashboard":
    st.metric("Coins", st.session_state.coins)
    st.metric("Streak", st.session_state.streak)
    st.metric("Rank", rank)

# ... (Các menu khác thêm tương tự, đảm bảo dùng elif và thụt đầu dòng đúng)
