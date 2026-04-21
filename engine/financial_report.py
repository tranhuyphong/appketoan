def generate_report(data):

    revenue = sum(x["amount"] for x in data if x["type"] == "revenue")
    expense = sum(x["amount"] for x in data if x["type"] == "expense")
    profit = revenue - expense

    return {
        "revenue": revenue,
        "expense": expense,
        "profit": profit
    }
