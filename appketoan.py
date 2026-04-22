import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

# ================= 1. CẤU HÌNH TRANG (PHẢI Ở ĐẦU) =================
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

# ================= 4. HÀM RENDER MAP (ZIGZAG & CLICK) =================
def render_duolingo_pro(unit_id, lessons):
    html = f"""
    <style>
    .map {{ display: flex; flex-direction: column; align-items: center; gap: 35px; padding: 20px; }}
    .row {{ width: 100%; display: flex; }}
    .left {{ justify-content: flex-start; padding-left: 20%; }}
    .right {{ justify-content: flex-end; padding-right: 20%; }}
    .node {{ 
        width: 75px; height: 75px; border-radius: 50%; display: flex; align-items: center; 
        justify-content: center; font-weight: bold; font-size: 20px; color: white; 
        cursor: pointer; transition: all 0.25s ease; position: relative; 
    }}
    .node:hover {{ transform: scale(1.15); }}
    .done {{ background: linear-gradient(145deg, #22c55e, #16a34a); }}
    .current {{ 
        background: linear-gradient(145deg, #3b82f6, #2563eb); 
        animation: pulse 1.5s infinite; box-shadow: 0 0 20px #3b82f6; 
    }}
    .locked {{ background: #334155; opacity: 0.4; cursor: not-allowed; }}
    .boss {{ background: linear-gradient(145deg, #f59e0b, #d97706); box-shadow: 0 0 25px gold; }}
    @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} 100% {{ transform: scale(1); }} }}
    .line {{ width: 6px; height: 40px; background: #475569; }}
    </style>
    <div class="map">
    """
    for i, lesson in enumerate(lessons):
        status = lesson["status"]
        cls = "node"
        if lesson.get("boss"): cls += " boss"
        elif status == "done": cls += " done"
        elif status == "current": cls += " current"
        else: cls += " locked"

        side = "left" if i % 2 == 0 else "right"
        # JavaScript để gửi message về Streamlit khi click
        click_js = f"window.parent.postMessage('{unit_id}|{i}', '*')" if status != "locked" else ""
        
        html += f"""
        <div class="row {side}">
            <div class="{cls}" onclick="{click_js}">
                {i+1}
            </div>
        </div>
        """
        if i < len(lessons) - 1:
            html += "<div class='line'></div>"
    html += "</div>"
    
    # Thành phần nhận sự kiện click từ JavaScript (Ảnh 2)
    components.html(f"""
        {html}
        <script>
        window.addEventListener("message", (event) => {{
            const data = event.data;
            if (data && typeof data === 'string' && data.includes('|')) {{
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: data
                }}, "*");
            }}
        }});
        </script>
    """, height=600)

def load_progress():
    try:
        res = supabase.table("users_progress").select("*").eq("email", st.session_state.user).execute()
        return {r["lesson_id"]: r for r in res.data}
    except: return {}

def save_progress(lesson_id, score):
    try:
        supabase.table("users_progress").upsert({
            "email": st.session_state.user, "lesson_id": lesson_id,
            "status": "done", "score": score, "last_learned": str(datetime.date.today())
        }).execute()
    except Exception as e: print("Lỗi lưu tiến trình:", e)

def save_coins():
    if "user" in st.session_state and st.session_state.user:
        try:
            supabase.table("users").upsert({
                "email": st.session_state.user, "coins": st.session_state.coins
            }).execute()
        except Exception as e: print(f"Lưu coin thất bại: {e}")

# ================= 5. KHỞI TẠO SESSION STATE =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins": 100, "streak": 0, "last_login": "", "percent": None,
        "lesson_progress": {}, "current_lesson": None, "q_index": 0,
        "chat_history": [], "skills": {}, "learned_lessons": [], "daily_learn": 0
    })

# ================= 6. ĐĂNG NHẬP / ĐĂNG KÝ =================
if "user" not in st.session_state:
    st.title("🚀 PHONG AI ACCOUNTING")
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
    with tab1:
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        if st.button("Đăng nhập"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": pw})
                if res.user:
                    st.session_state.user = res.user.email
                    st.rerun()
            except: st.error("Sai tài khoản hoặc mật khẩu!")
    with tab2:
        reg_email = st.text_input("Email đăng ký")
        reg_pw = st.text_input("Password đăng ký", type="password")
        if st.button("Thực hiện Đăng ký"):
            try:
                supabase.auth.sign_up({"email": reg_email, "password": reg_pw})
                st.success("Đăng ký xong! Hãy qua tab Đăng nhập.")
            except Exception as e: st.error(f"Lỗi: {e}")
    st.stop()

# ================= 7. TẢI DỮ LIỆU TIẾN TRÌNH =================
if "progress_loaded" not in st.session_state:
    db_progress = load_progress()
    for l_id, data in db_progress.items():
        st.session_state.lesson_progress[l_id] = {"answers": {}, "submitted": True, "score": data.get("score", 0)}
    st.session_state.progress_loaded = True

# Thưởng đăng nhập hàng ngày
today = str(datetime.date.today())
if st.session_state.last_login != today:
    st.session_state.coins += 20
    st.session_state.last_login = today
    save_coins()

# ================= 8. GIAO DIỆN CHÍNH =================
coins = st.session_state.coins
rank = "🥉 Intern" if coins < 100 else "🥈 Junior" if coins < 300 else "🥇 Senior" if coins < 600 else "👑 Manager"

st.sidebar.markdown(f"### 🎖️ Rank: {rank}")
st.sidebar.markdown(f"### 💰 Coins: {coins}")

menu = st.sidebar.radio("Menu", [
    "📘 Học", "🎓 Lớp học AI (Quiz)", "🎓 Lớp học AI (Chat)", "💼 Đi làm",
    "🧾 Case Study", "📊 Dashboard", "📊 Financial Report", "🤖 Chấm bút toán",
    "📚 Từ điển", "🚨 Fraud Detection", "🏆 Leaderboard"
])

# ================= 9. LOGIC CÁC MENU =================

if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    # --- LOGIC HIỂN THỊ LESSON KHI ĐƯỢC CLICK (Ảnh 5) ---
    if st.session_state.get("current_lesson"):
        lesson = st.session_state.current_lesson
        st.markdown(f"## 📖 {lesson['title']}")
        st.write(lesson["content"])
        
        # Phần Quiz trong bài học
        l_id = st.session_state.get("current_lesson_id", "temp")
        prog = st.session_state.lesson_progress.get(l_id, {"submitted": False})
        
        if not prog.get("submitted"):
            correct_count = 0
            for i, q in enumerate(lesson.get("quiz", [])):
                ans = st.radio(q["question"], q["options"], key=f"quiz_{i}")
                if ans == q["options"][q["answer"]]: correct_count += 1
            
            if st.button("🚀 Hoàn thành bài học"):
                score = int((correct_count / len(lesson["quiz"])) * 100) if lesson.get("quiz") else 100
                st.session_state.lesson_progress[l_id] = {"submitted": True, "score": score}
                if score >= 70:
                    st.session_state.coins += 20
                    save_progress(l_id, score)
                save_coins()
                st.rerun()
        else:
            st.success(f"Bạn đã hoàn thành bài này với {prog['score']}% điểm!")

        if st.button("❌ Đóng"):
            st.session_state.current_lesson = None
            st.rerun()
        st.divider()

    # --- RENDER MAP ---
    for level in curriculum:
        # SỬA LỖI KEYERROR: 'level' (Ảnh 1)
        level_name = level.get('level', level.get('name', 'Cấp độ mới'))
        
        required = level.get("unlock_coins", 0)
        unlocked = st.session_state.coins >= required

        if not unlocked:
            st.markdown(f"## 🔒 {level_name} (Cần {required} 💰)")
            continue
        
        st.markdown(f"## 🔓 {level_name}")
        for module in level.get("modules", []):
            st.markdown(f"### 📚 {module['name']}")
            
            # BUILD LESSON NODES (Ảnh 3)
            lesson_nodes = []
            prev_passed = True
            for i, lesson in enumerate(module["lessons"]):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"
                if l_id not in st.session_state.lesson_progress:
                    st.session_state.lesson_progress[l_id] = {"submitted": False, "score": 0}
                
                prog = st.session_state.lesson_progress[l_id]
                if prog["submitted"] and prog["score"] >= 70:
                    status = "done"
                elif prev_passed:
                    status = "current"
                else:
                    status = "locked"
                
                lesson_nodes.append({
                    "status": status,
                    "boss": (i == len(module["lessons"]) - 1) # Bài cuối là Boss
                })
                prev_passed = (status == "done")

            # RENDER MAP & XỬ LÝ CLICK (Ảnh 4)
            clicked = render_duolingo_pro(module["name"], lesson_nodes)
            
            if clicked:
                unit, index = clicked.split("|")
                if unit == module["name"]:
                    idx = int(index)
                    sel_lesson = module["lessons"][idx]
                    st.session_state.current_lesson = sel_lesson
                    st.session_state.current_lesson_id = f"{level_name}_{module['name']}_{sel_lesson['title']}"
                    st.rerun()

elif menu == "🎓 Lớp học AI (Quiz)":
    if len(question_bank) > 0:
        q = question_bank[st.session_state.q_index % len(question_bank)]
        st.subheader(q["question"])
        ans = st.radio("Chọn đáp án:", q["options"])
        if st.button("Nộp"):
            if q["options"].index(ans) == q["correct"]:
                st.session_state.streak += 1
                reward = min(10 + st.session_state.streak * 2, 30)
                st.success(f"Chính xác! +{reward} coins")
                st.session_state.coins += reward
            else:
                st.session_state.streak = 0
                st.error("Sai rồi! -5 coins")
                st.session_state.coins -= 5
            st.info(q["explain"])
            save_coins()
        if st.button("➡️ Câu tiếp"):
            st.session_state.q_index += 1
            st.rerun()

elif menu == "🎓 Lớp học AI (Chat)":
    st.header("💬 Chat với Giảng viên AI")
    if not st.session_state.chat_history:
        st.session_state.chat_history = [{"role": "assistant", "content": "Chào bạn, hãy trả lời: Phương trình kế toán cơ bản là gì?"}]
    for m in st.session_state.chat_history:
        st.chat_message(m["role"]).write(m["content"])
    u_input = st.chat_input("Nhập câu trả lời...")
    if u_input:
        st.session_state.chat_history.append({"role": "user", "content": u_input})
        reply = classroom_chat(st.session_state.chat_history, u_input)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        if "đúng" in reply.lower(): st.session_state.coins += 10
        save_coins()
        st.rerun()

elif menu == "💼 Đi làm":
    st.header("🏢 Career Mode - Đi làm thực tế")
    if "work_day" not in st.session_state: 
        st.session_state.update({"work_day": 1, "performance": 100})
    st.info(f"📅 Ngày {st.session_state.work_day} | 📊 Hiệu suất: {st.session_state.performance}%")
    role_key = rank.split(" ")[1] if " " in rank else rank
    tasks = career_tasks.get(role_key, career_tasks.get("Intern", []))
    if tasks:
        task = random.choice(tasks)
        st.subheader("Nhiệm vụ hôm nay:")
        st.write(task["desc"])
        opts = [task["correct"]] + task["wrong"]
        random.shuffle(opts)
        choice = st.radio("Hướng xử lý:", opts)
        if st.button("🚀 Giải quyết"):
            if choice == task["correct"]:
                st.success("Sếp khen! +30 coins")
                st.session_state.coins += 30
            else:
                st.error("Bị nhắc nhở! -20 coins")
                st.session_state.coins -= 20
            st.session_state.work_day += 1
            save_coins()

elif menu == "📊 Dashboard":
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Tổng Coins", st.session_state.coins)
    col2.metric("🔥 Chuỗi học (Streak)", st.session_state.streak)
    col3.metric("🎖️ Cấp bậc", rank)
    
elif menu == "🏆 Leaderboard":
    st.header("🏆 Bảng Xếp Hạng")
    try:
        res = supabase.table("users").select("email, coins").order("coins", desc=True).limit(10).execute()
        df = pd.DataFrame(res.data)
        st.table(df)
    except: st.error("Không thể tải bảng xếp hạng.")

st.sidebar.divider()
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
