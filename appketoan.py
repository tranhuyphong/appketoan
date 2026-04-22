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

# ================= 3. SUPABASE =================
SUPABASE_URL = "https://wjwtowmdcdkpryxcqqty.supabase.co"
SUPABASE_KEY = "YOUR_KEY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= 4. FIXED MAP =================
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
        cls = "node"

        if lesson["type"] == "boss":
            cls += " boss"
        elif lesson["type"] == "exam":
            cls += " exam"

        cls += f" {lesson['status']}"

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

        if i < len(lessons)-1:
            html += "<div class='line'></div>"

    html += "</div>"

    components.html(f"""
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

    return st.session_state.get("clicked_node")

# ================= 5. SESSION =================
if "coins" not in st.session_state:
    st.session_state.update({
        "coins": 100,
        "lesson_progress": {},
        "current_lesson": None
    })

# ================= 6. UI =================
menu = st.sidebar.radio("Menu", ["📘 Học"])

# ================= 7. LEARNING MAP =================
if menu == "📘 Học":
    st.header("🗺️ Learning Map")

    if st.session_state.get("current_lesson"):
        lesson = st.session_state.current_lesson
        st.subheader(lesson["title"])
        st.write(lesson["content"])

        if st.button("❌ Đóng"):
            st.session_state.current_lesson = None
            st.rerun()

    for level in curriculum:
        level_name = level["level"]
        required = level.get("unlock_coins", 0)
        unlocked = st.session_state.coins >= required

        st.markdown(f"## {'🔓' if unlocked else '🔒'} {level_name} (Cần {required})")

        for module in level["modules"]:
            st.markdown(f"### {module['name']}")

            lesson_nodes = []
            prev_passed = True

            for i, lesson in enumerate(module["lessons"]):
                l_id = f"{level_name}_{module['name']}_{lesson['title']}"
                prog = st.session_state.lesson_progress.get(l_id, {"submitted": False, "score": 0})

                if prog["submitted"] and prog["score"] >= 70:
                    status = "done"
                elif prev_passed and unlocked:
                    status = "current"
                else:
                    status = "locked"

                lesson_nodes.append({
                    "status": status,
                    "type": "lesson",
                    "label": str(i+1)
                })

                prev_passed = (status == "done")

            lesson_nodes.append({
                "status": "current" if prev_passed else "locked",
                "type": "boss",
                "label": "👑"
            })

            if module == level["modules"][-1]:
                lesson_nodes.append({
                    "status": "locked",
                    "type": "exam",
                    "label": "🎓"
                })

            clicked = render_duolingo_pro(module["name"], lesson_nodes)

            # FIX CLICK
            if st.session_state.get("clicked_node"):
                unit, index = st.session_state.clicked_node.split("|")
                st.session_state.clicked_node = None

                if unit == module["name"]:
                    idx = int(index)
                    if idx < len(module["lessons"]):
                        st.session_state.current_lesson = module["lessons"][idx]
                        st.rerun()

# ================= CLICK HANDLER =================
if "clicked_node" not in st.session_state:
    st.session_state.clicked_node = None

query = st.query_params
if "value" in query:
    st.session_state.clicked_node = query["value"]
