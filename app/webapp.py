import streamlit as st
from backend.genai import ask_agent

# Page settings and title 
st.set_page_config(page_title="AI Predictor", page_icon="🤖", layout="centered")
st.title("GasPredictor")
st.write("Ask a question about the model or gas price next week!")

# Chat-section (LLM-agent)
st.subheader("Chat")

prompt = st.text_input(
    "Write your question:",
    placeholder="Eg: Should i fill up my tank this week?"
)

if st.button("Send to LLM"):
    if not prompt.strip():
        st.warning("Write a question first!")
    else:
        with st.spinner(f"The agent is thinking..."):
            llm_response = ask_agent(prompt)

        st.success("Response from the agent:")
        st.write(llm_response)


st.markdown("---")
st.markdown("""
### ℹ️ About the Application
This application is a demo that lets you interact with an LLM that has access to a 
model that predicts next weeks gas prices. 
""")
