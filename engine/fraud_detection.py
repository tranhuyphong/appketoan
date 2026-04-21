from openai import OpenAI

def detect_fraud(data):

    try:
        client = OpenAI()

        prompt = f"""
Bạn là kiểm toán viên.

Phân tích dữ liệu kế toán sau và tìm dấu hiệu gian lận, bất thường:

{data}

Trả lời ngắn gọn dạng bullet:
- ...
- ...
"""

        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return [res.choices[0].message.content]

    except Exception as e:
        # fallback nếu AI lỗi
        alerts = []

        for t in data:
            if t["amount"] > 6000:
                alerts.append(f"Giao dịch lớn bất thường: {t['amount']}")

        expense_total = sum(x["amount"] for x in data if x["type"] == "expense")

        if expense_total > 5000:
            alerts.append("Chi phí cao bất thường")

        if len(alerts) == 0:
            alerts.append("Không phát hiện gian lận (rule-based)")

        return alerts
