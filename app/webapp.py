import streamlit as st
from backend.genai import ask_agent

# Page settings and title 
st.set_page_config(page_title="GasPredictor", page_icon="🤖", layout="centered")
st.title("GasPredictor")
st.write("Ask a question about the model or gas price next week!")

prompt = st.chat_input(
    "Write your question:"
)

if prompt:
    with st.spinner(f"The agent is thinking..."):
        llm_response = ask_agent(prompt)

    st.success(llm_response)
    

