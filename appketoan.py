import streamlit as st
import random
import datetime
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client

st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ================= IMPORT =================
try:
    from data.career_tasks import career_tasks
    from data.curriculum import curriculum
    from data.question_bank import question_bank
    from data.dictionary import dictionary
    from data.case_study import case_studies
    from engine.classroom_ai import classroom_chat
except:
    curriculum = []
    question_bank = []

# ================= SUPABASE =================
SUPABASE_URL = "YOUR_URL"
SUPABASE_KEY = "YOUR_KEY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= UI MAP =================
def render_duolingo_pro(unit_id, lessons):
    html = f"""
    <style>
    .map {{ display:flex; flex-direction:column; align-items:center; gap:30px; }}
    .row {{ width:100%; display:flex; }}
    .left {{ justify-content:flex-start; padding-left:15%; }}
    .right {{ justify-content:flex-end; padding-right:15%; }}

    .node {{
        width:80px;height:80px;border-radius:50%;
        display:flex;align-items:center;justify-content:center;
        font-weight:bold;font-size:22px;color:white;
        cursor:pointer;transition:0.3s;
    }}

    .node:hover {{ transform:scale(1.2); }}

    .done {{ background:#22c55e; box-shadow:0 0 15px #22c55e; }}
    .current {{ background:#3b82f6; animation:pulse 1.5s infinite; }}
    .locked {{ background:#334155; opacity:0.3; cursor:not-allowed; }}
    .boss {{ background:#f59e0b; box-shadow:0 0 25px gold; }}

    @keyframes pulse {{
        0%{{transform:scale(1)}}
        50%{{transform:scale(1.15)}}
        100%{{transform:scale(1)}}
    }}

    .line {{ width:6px;height:40px;background:#475569; }}
    </style>

    <div class="map">
    """

    for i, lesson in enumerate(lessons):
        cls = "node"
        if lesson.get("boss"):
            cls += " boss"
        elif lesson["status"] == "done":
            cls += " done"
        elif lesson["status"] == "current":
            cls += " current"
        else:
            cls += " locked"

        side = "left" if i % 2 == 0 else "right"

        click = ""
        if lesson["status"] != "locked":
            click = f"onclick=\\"selectLesson('{unit_id}', {i})\\""

        html += f"""
        <div class="row {side}">
            <div class="{cls}" {click}>{i+1}</div>
        </div>
        """

        if i < len(lessons) - 1:
            html += "<div class='line'></div>"

    html += """
    </div>

    <script>
    function selectLesson(unit, index){
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: unit + "|" + index
        }, "*");
    }
    </script>
    """

    return components.html(html, height=650)

# ================= HELPERS =================
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
            "score": score
        }).execute()
    except:
        pass

# ================= SESSION =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins":100,
        "lesson_progress":{},
        "current_lesson":None
    })

# ================= LOGIN =================
if "user" not in st.session_state:
    st.title("LOGIN")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            res = supabase.auth.sign_in_with_password({"email":email,"password":pw})
            st.session_state.user = res.user.email
            st.rerun()
        except:
            st.error("Sai")
    st.stop()

# ================= LOAD PROGRESS =================
if "loaded" not in st.session_state:
    db = load_progress()
    for k,v in db.items():
        st.session_state.lesson_progress[k] = {"submitted":True,"score":v.get("score",0)}
    st.session_state.loaded = True

# ================= SIDEBAR =================
st.sidebar.markdown(f"💰 {st.session_state.coins}")
menu = st.sidebar.radio("Menu", ["📘 Học","🎓 Quiz"])

# ================= LEARNING =================
if menu == "📘 Học":

    st.header("Learning Map")

    # ===== HIỂN THỊ LESSON =====
    if st.session_state.get("current_lesson"):
        lesson = st.session_state.current_lesson
        st.subheader(lesson["title"])
        st.write(lesson["content"])

        l_id = st.session_state.current_lesson_id
        prog = st.session_state.lesson_progress.get(l_id, {"submitted":False})

        if not prog["submitted"]:
            correct = 0
            for i,q in enumerate(lesson.get("quiz",[])):
                ans = st.radio(q["question"], q["options"], key=f"q{i}")
                if ans == q["options"][q["answer"]]:
                    correct += 1

            if st.button("Hoàn thành"):
                score = int(correct/len(lesson["quiz"])*100) if lesson.get("quiz") else 100
                st.session_state.lesson_progress[l_id] = {"submitted":True,"score":score}

                if score >= 70:
                    st.session_state.coins += 20
                    save_progress(l_id, score)

                st.rerun()
        else:
            st.success("Đã hoàn thành")

        if st.button("Đóng"):
            st.session_state.current_lesson = None
            st.rerun()

    # ===== MAP =====
    for level in curriculum:
        level_name = level.get("level","Level")

        st.markdown(f"## {level_name}")

        for module in level.get("modules",[]):

            lesson_nodes = []
            prev = True

            for i,lesson in enumerate(module["lessons"]):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"

                if l_id not in st.session_state.lesson_progress:
                    st.session_state.lesson_progress[l_id] = {"submitted":False,"score":0}

                prog = st.session_state.lesson_progress[l_id]

                if prog["submitted"] and prog["score"]>=70:
                    status="done"
                elif prev:
                    status="current"
                else:
                    status="locked"

                lesson_nodes.append({
                    "status":status,
                    "boss": i==len(module["lessons"])-1
                })

                prev = (status=="done")

            clicked = render_duolingo_pro(module["name"], lesson_nodes)

            if isinstance(clicked,str) and "|" in clicked:
                unit, index = clicked.split("|")

                if unit == module["name"]:
                    idx = int(index)
                    sel = module["lessons"][idx]

                    st.session_state.current_lesson = sel
                    st.session_state.current_lesson_id = f"{level_name}_{module['name']}_{sel['title']}"
                    st.rerun()

# ================= QUIZ =================
elif menu == "🎓 Quiz":
    if question_bank:
        q = random.choice(question_bank)
        st.write(q["question"])
        ans = st.radio("Chọn", q["options"])
        if st.button("Submit"):
            if q["options"].index(ans) == q["correct"]:
                st.success("Đúng")
                st.session_state.coins += 10
            else:
                st.error("Sai")

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
