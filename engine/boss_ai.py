import random

def boss_msg(action):
    if action == "ask_question":
        questions = [
            "Chi phí là gì?",
            "Tài sản là gì?",
            "Doanh thu là gì?",
            "Nợ phải trả là gì?",
            "Vốn chủ sở hữu là gì?"
        ]
        return random.choice(questions)

    elif action == "react_correct":
        return random.choice([
            "🔥 Chuẩn rồi!",
            "💪 Tốt lắm!",
            "👑 Ngươi khá đấy!"
        ])

    elif action == "react_wrong":
        return random.choice([
            "💀 Sai rồi!",
            "❌ Học lại đi!",
            "😈 Ta mạnh hơn ngươi!"
        ])

    return "..."
