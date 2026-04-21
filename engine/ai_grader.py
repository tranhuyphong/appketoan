import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def grade(entry):
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":f"Kiểm tra bút toán: {entry}"}]
    )
    return res.choices[0].message.content
