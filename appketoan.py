import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

# ================= 1. CONFIG =================
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= 2. IMPORT =================
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
    curriculum = []
    question_bank = []

# 👉 FIX QUAN TRỌNG: đảm bảo curriculum đúng
try:
    from data.learning_path import learning_path
    curriculum = learning_path
except:
    pass

# ================= 3. SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "YOUR_KEY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= 4. RENDER MAP (FIX CLICK) =================
def render_duolingo_pro(unit_id, lessons):
    html = """
    <style>
    .map { display: flex; flex-direction: column; align-items: center; gap: 35px; }
    .row { width: 100%; display: flex; }
    .left { justify-content: flex-start; padding-left: 20%; }
    .right { justify-content: flex-end; padding-right: 20%; }

    .node {
        width: 80px; height: 80px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 22px; color: white;
        cursor: pointer;
    }

    .done { background: #22c55e; }
    .current { background: #3b82f6; }
    .locked { background: #334155; opacity: 0.4; cursor: not-allowed; }
    .boss { background: gold; color: black; }
    .exam { background: purple; }

    .line { width: 6px; height: 40px; background: #475569; }
    </style>

    <div class="map">
    """

    for i, lesson in enumerate(lessons):
        cls = f"node {lesson['status']}"

        if lesson["type"] == "boss":
            cls += " boss"
        elif lesson["type"] == "exam":
            cls += " exam"

        side = "left" if i % 2 == 0 else "right"
        label = lesson["label"]

        click = f"sendClick('{unit_id}|{i}')" if lesson["status"] != "locked" else ""

        html += f"""
        <div class="row {side}">
            <div class="{cls}" onclick="{click}">
                {label}
            </div>
        </div>
        """

        if i < len(lessons) - 1:
            html += "<div class='line'></div>"

    html += "</div>"

    # 🔥 FIX CLICK VALUE
    return components.html(f"""
    {html}
    <script>
    function sendClick(val){{
        window.parent.postMessage({{
            type: "streamlit:setComponentValue",
            value: val
        }}, "*");
    }}
    </script>
    """, height=600)

# ================= DB =================
def load_progress():
    try:
        res = supabase.table("users_progress").select("*").eq("email", st.session_state.user).execute()
        return {r["lesson_id"]: r for r in res.data}
    except:
        return {}

def save_progress(lesson_id, score):
    try:
        supabase.table("users_progress").upsert({
            "email": st.session_state.user,
            "lesson_id": lesson_id,
            "status": "done",
            "score": score,
            "last_learned": str(datetime.date.today())
        }).execute()
    except:
        pass

def save_coins():
    try:
        supabase.table("users").upsert({
            "email": st.session_state.user,
            "coins": st.session_state.coins
        }).execute()
    except:
        pass

# ================= SESSION =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins": 100,
        "streak": 0,
        "last_login": "",
        "lesson_progress": {},
        "current_lesson": None,
        "q_index": 0,
        "chat_history": []
    })

# ================= LOGIN =================
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
        except:
            st.error("Sai tài khoản!")

    st.stop()

# ================= LOAD PROGRESS =================
if "progress_loaded" not in st.session_state:
    db = load_progress()
    for l_id, data in db.items():
        st.session_state.lesson_progress[l_id] = {
            "submitted": True,
            "score": data.get("score", 0)
        }
    st.session_state.progress_loaded = True

# ================= DAILY =================
today = str(datetime.date.today())
if st.session_state.last_login != today:
    st.session_state.coins += 20
    st.session_state.last_login = today
    save_coins()

# ================= UI =================
coins = st.session_state.coins
st.sidebar.markdown(f"💰 Coins: {coins}")

menu = st.sidebar.radio("Menu", ["📘 Học", "🏆 Leaderboard"])

# ================= LEARNING MAP =================
if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    if not curriculum:
        st.error("❌ Curriculum chưa load!")
        st.stop()

    if st.session_state.current_lesson:
        lesson = st.session_state.current_lesson
        st.subheader(lesson["title"])
        st.write(lesson["content"])

        if st.button("Đóng"):
            st.session_state.current_lesson = None
            st.rerun()

    for level in curriculum:

        level_name = level.get("level") or level.get("name") or "Level"
        required = level.get("unlock_coins", 0)
        unlocked = coins >= required

        st.markdown(f"## {'🔓' if unlocked else '🔒'} {level_name} (Cần {required}💰)")

        for module in level.get("modules", []):
            st.markdown(f"### 📚 {module['name']}")

            lesson_nodes = []
            prev = True

            for i, lesson in enumerate(module["lessons"]):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"
                prog = st.session_state.lesson_progress.get(l_id, {"submitted": False, "score": 0})

                if prog["submitted"] and prog["score"] >= 70:
                    status = "done"
                elif prev and unlocked:
                    status = "current"
                else:
                    status = "locked"

                lesson_nodes.append({
                    "status": status,
                    "type": "lesson",
                    "label": str(i + 1)
                })

                prev = (status == "done")

            # BOSS
            lesson_nodes.append({
                "status": "current" if prev else "locked",
                "type": "boss",
                "label": "👑"
            })

            # EXAM
            if module == level["modules"][-1]:
                lesson_nodes.append({
                    "status": "locked",
                    "type": "exam",
                    "label": "🎓"
                })

            clicked = render_duolingo_pro(module["name"], lesson_nodes)

            # 🔥 FIX CLICK
            if clicked:
                unit, index = clicked.split("|")
                if unit == module["name"]:
                    idx = int(index)
                    if idx < len(module["lessons"]):
                        sel = module["lessons"][idx]
                        st.session_state.current_lesson = sel
                        st.rerun()

# ================= LEADERBOARD =================
elif menu == "🏆 Leaderboard":
    try:
        res = supabase.table("users").select("email, coins").execute()
        st.table(pd.DataFrame(res.data))
    except:
        st.error("Lỗi load bảng xếp hạng")

# ================= LOGOUT =================
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()
