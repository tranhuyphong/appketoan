import random

def boss_msg(user_input):

    questions = [
        "Tài sản là gì?",
        "Phân biệt tài sản và nợ?",
        "Tiền mặt thuộc loại gì?",
        "Doanh thu là gì?",
        "Chi phí là gì?"
    ]

    # câu đầu
    if user_input == "ask_question":
        return random.choice(questions)

    # logic trả lời
    if "tài sản" in user_input.lower():
        return "✅ Đúng! Tiếp: Doanh thu là gì?"
    else:
        return "❌ Sai! Thử lại: Doanh thu là gì?"
