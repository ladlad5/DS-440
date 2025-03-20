import streamlit as st
from ollama import chat
from ollama import ChatResponse
import re
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'patient_info' not in st.session_state:
    st.session_state.patient_info = None

def generate_response(user_input):
    st.toast('Generating response')
    with st.spinner("Generating response", show_time=True):
        response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=[
    {
        'role': 'user',
        'content': user_input,
    },
        ])
        response_text = response['message']['content']
        think_texts = re.findall(r"<think>(.*?)</think>", response_text, flags=re.DOTALL) #extracts deep_think
        think_texts = "\n\n".join(think_texts).strip() 
        clean_response = re.sub(r"<think>.*?</think>", '', response_text, flags = re.DOTALL).strip()
        return clean_response
    return f"This is a response to: {user_input}" 

st.set_page_config(page_title="MediHelp", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color:rgb(0, 82, 245);
    }
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    .chat-box {
        display: flex;
        flex-direction: column;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 70%;
        word-wrap: break-word;
        color: black; /* Set text color to black */
    }
    .user-bubble {
        background-color: #DCF8C6;
        align-self: flex-end;
        text-align: right;
    }
    .bot-bubble {
        background-color:rgb(255, 255, 255);
        align-self: flex-start;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: center;'>MediHelp</h2>", unsafe_allow_html=True)

st.markdown("<h3 style='color: white;'>Patient Information</h3>", unsafe_allow_html=True)
with st.form(key="patient_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
         patient_id = st.text_input("Enter Patient ID:")
    submitted_patient = st.form_submit_button("Submit Patient ID")

if submitted_patient and patient_id:
    if patient_id == "123":
         patient_name = "John Doe"
         patient_age = "30"
    else:
         patient_name = "Jane Smith"
         patient_age = "40"
    st.session_state.patient_info = {"id": patient_id, "name": patient_name, "age": patient_age}

if st.session_state.patient_info:
    col1, col2 = st.columns(2)
    with col1:
         st.markdown(f"<p style='color: white;'>Patient Name: {st.session_state.patient_info['name']}</p>", unsafe_allow_html=True)
    with col2:
         st.markdown(f"<p style='color: white;'>Patient Age: {st.session_state.patient_info['age']}</p>", unsafe_allow_html=True)

if st.button("Clear Chat History"):
    st.session_state.messages = []

with st.container():
    for msg in st.session_state.messages:
        if msg["sender"] == "user":
            st.markdown(
                f"<div class='chat-box' style='display: flex; justify-content: flex-end;'>"
                f"<div class='chat-bubble user-bubble'>{msg['text']}</div></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='chat-box' style='display: flex; justify-content: flex-start;'>"
                f"<div class='chat-bubble bot-bubble'>{msg['text']}</div></div>",
                unsafe_allow_html=True
            )

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Enter your message:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append({"sender": "user", "text": user_input})
    response = generate_response(user_input)
    st.session_state.messages.append({"sender": "bot", "text": response})
    st.rerun()
