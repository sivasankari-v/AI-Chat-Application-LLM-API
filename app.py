import streamlit as st
import os
from groq import Groq
from datetime import datetime

# Page Config
st.set_page_config(page_title="AI Chat App - Sivasankari V", page_icon="🤖", layout="wide")

# Sidebar - All Module 3 Requirements
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("**Module 3: LLM APIs**")

    api_key = st.text_input("Groq API Key (Free)", type="password", help="Get free key from console.groq.com")

    model = st.selectbox("Select Model", ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3-32b", "llama-3.1-8b-instant"])

    temperature = st.slider("Temperature (Creativity)", 0.0, 2.0, 0.7)
    max_tokens = st.slider("Max Tokens (Cost Control)", 100, 4000, 1024)

    st.divider()
    custom_instruction = st.text_area("Custom System Instruction",
                                      value="You are a helpful AI assistant built by Sivasankari V, B.TECH AI & DS student. Be friendly and concise.",
                                      height=120)

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.token_count = 0
        st.rerun()

    st.divider()
    st.metric("Total Tokens Used", st.session_state.get("token_count", 0))
    st.caption("Cost Management: Low cost with Groq API")

# Main App
st.title("🤖 AI Chat Application")
st.caption("Built for Module 3 - LLM APIs & Application Development | Sivasankari V")

# Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []
if "token_count" not in st.session_state:
    st.session_state.token_count = 0

# Display History - (Chat History Requirement)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask anything..."):
    if not api_key:
        st.error("⚠️ Please enter Groq API Key in sidebar! Get free from console.groq.com")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response with Error Handling
    try:
        client = Groq(api_key=api_key)

        # Prepare messages with System/User/Assistant structure
        api_messages = [{"role": "system", "content": custom_instruction}]
        for m in st.session_state.messages:
            api_messages.append({"role": m["role"], "content": m["content"]})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                ai_reply = response.choices[0].message.content
                usage = response.usage
                st.session_state.token_count += usage.total_tokens

                st.markdown(ai_reply)
                st.caption(f"Tokens: {usage.total_tokens} | Model: {model}")

        # Add assistant to history
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Check API Key, Internet, or try again. Robust error handling implemented.")
