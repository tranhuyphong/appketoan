import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def boss_msg(task):
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": f"Giao việc kế toán: {task['description']}"}
        ]
    )
    return res.choices[0].message.content
