import streamlit as st
from data.question_bank import question_bank
from engine.ai_teacher import teacher_explain
from engine.progress_tracker import update_progress
from engine.classroom_ai import classroom_chat
from data.curriculum import curriculum
from data.dictionary import dictionary
import sys
import os
sys.path.append(os.path.dirname(__file__))

from data.jobs import jobs
from engine.boss_ai import boss_msg
from engine.ai_grader import grade
from data.case_study import case_studies

# ===== CONFIG =====
st.set_page_config(page_title="Phong AI Accounting", layout="wide")

# ===== STATE =====
if "coins" not in st.session_state:
    st.session_state.coins = 100

# ===== HEADER =====
st.title("🚀 PHONG AI ACCOUNTING")

st.metric("💰 Coins", st.session_state.coins)
st.subheader("📊 Học lực")

if "skills" in st.session_state:
    for skill, data in st.session_state.skills.items():
        total = data["correct"] + data["wrong"]

        if total > 0:
            acc = data["correct"] / total * 100
        else:
            acc = 0

        st.write(f"{skill}: {round(acc,1)}%")

# ===== MENU =====
menu = st.sidebar.radio("Menu", [
    "📘 Học",
    "🎓 Lớp học AI (Quiz)",   # 👈 học chuẩn
    "🎓 Lớp học AI (Chat)",   # 👈 chat realtime
    "💼 Đi làm",
    "🧾 Case Study",
    "📊 Dashboard",
    "🤖 Chấm bút toán",
    "📚 Từ điển"
])


# ================= HỌC =================
if menu == "📘 Học":
    st.write("Phần học cơ bản")

# ================= QUIZ =================
elif menu == "🎓 Lớp học AI (Quiz)":

    st.header("🎓 Lớp học chuẩn giáo dục")

    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    q = question_bank[st.session_state.q_index]

    st.subheader(f"Câu hỏi {q['id']}")
    st.write(q["question"])

    answer = st.radio("Chọn đáp án:", q["options"])

    if st.button("Nộp bài"):

        correct = q["options"].index(answer) == q["correct"]

        update_progress(q["skill"], correct, st.session_state)

        if correct:
            st.success("✅ Đúng +10 coins")
            st.session_state.coins += 10

            st.info(q["explain"])

            if st.button("Câu tiếp"):
                st.session_state.q_index += 1
                st.rerun()

        else:
            st.error("❌ Sai -5 coins")
            st.session_state.coins -= 5

            hint = teacher_explain(q["question"], answer)
            st.warning("🤖 Gợi ý:")
            st.write(hint)


# ================= CHAT AI =================
elif menu == "🎓 Lớp học AI (Chat)":

    st.header("🎓 Lớp học AI (Real-time)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hôm nay học phương trình kế toán.\n\n❓ Tài sản = ?"
            }
        ]

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"🧑‍🎓 **Bạn:** {msg['content']}")
        else:
            st.markdown(f"👨‍🏫 **Giáo viên:** {msg['content']}")

    st.divider()

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Nhập câu trả lời")
        submit = st.form_submit_button("Gửi")

    if submit and user_input.strip() != "":
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        reply = classroom_chat(
            st.session_state.chat_history,
            user_input
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": reply
        })

        if "đúng" in reply.lower():
            st.session_state.coins += 10
        else:
            st.session_state.coins -= 5

        st.rerun()

    if st.button("🔄 Reset"):
        st.session_state.chat_history = []
        st.rerun()


# ================= TỪ ĐIỂN =================
elif menu == "📚 Từ điển":

    st.header("📚 Từ điển")

    key = st.text_input("Nhập TK")

    if key in dictionary:
        st.success(dictionary[key])
    elif key != "":
        st.warning("Không tìm thấy")


# ================= ĐI LÀM =================
elif menu == "💼 Đi làm":

    task = jobs[0]["tasks"][0]

    st.subheader("Công việc hôm nay")
    st.info(boss_msg(task))

    user = st.text_input("Nhập bút toán")

    if st.button("Nộp task"):
        if user.lower() in task["correct"].lower():
            st.success("+20 coins")
            st.session_state.coins += 20
        else:
            st.error("-10 coins")
            st.session_state.coins -= 10
elif menu == "📊 Dashboard":

    import pandas as pd
    import matplotlib.pyplot as plt

    st.header("📊 Dashboard học lực")

    if "skills" not in st.session_state:
        st.warning("Chưa có dữ liệu học")
    else:
        data = []

        for skill, v in st.session_state.skills.items():
            total = v["correct"] + v["wrong"]
            acc = v["correct"] / total * 100 if total > 0 else 0

            data.append({
                "Skill": skill,
                "Correct": v["correct"],
                "Wrong": v["wrong"],
                "Accuracy": acc
            })

        df = pd.DataFrame(data)

        # ===== KPI =====
        st.subheader("📌 KPI")
        col1, col2, col3 = st.columns(3)

        col1.metric("Tổng kỹ năng", len(df))
        col2.metric("Trung bình %", round(df["Accuracy"].mean(), 1))
        col3.metric("Tổng câu đúng", df["Correct"].sum())

        # ===== BIỂU ĐỒ =====
        st.subheader("📈 Accuracy theo kỹ năng")

        fig, ax = plt.subplots()
        ax.bar(df["Skill"], df["Accuracy"])
        plt.xticks(rotation=30)

        st.pyplot(fig)

        # ===== BẢNG =====
        st.subheader("📋 Chi tiết")
        st.dataframe(df)
elif menu == "🧾 Case Study":

    st.header("🧾 Case Study thực tế")

    case = case_studies[0]

    st.subheader(case["title"])

    user_answers = []

    for i, trans in enumerate(case["transactions"]):
        st.write(f"{i+1}. {trans}")
        ans = st.text_input(f"Định khoản {i+1}", key=i)
        user_answers.append(ans)

    if st.button("Nộp bài Case"):

        score = 0

        for i in range(len(user_answers)):
            if user_answers[i].lower() in case["answers"][i].lower():
                score += 1

        st.success(f"🎯 Điểm: {score}/{len(case['answers'])}")

        # 🤖 AI NHẬN XÉT
        from engine.ai_teacher import teacher_explain

        feedback = teacher_explain(
            "Case study kế toán",
            str(user_answers)
        )

        st.info("🤖 Nhận xét:")
        st.write(feedback)


# ================= AI GRADER =================
elif menu == "🤖 Chấm bút toán":

    entry = st.text_area("Nhập bút toán")

    if st.button("Chấm"):
        st.write(grade(entry))
