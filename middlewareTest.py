import streamlit as st
import requests
import re
import pandas as pd

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'patient_info' not in st.session_state:
    st.session_state.patient_info = None
if 'show_help' not in st.session_state:
    st.session_state.show_help = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

patientDB = pd.read_csv('Patient_info_and_summary.csv')
patientDB["Patient ID"] = patientDB.index

if not st.session_state.logged_in:
    with st.form(key="login_form", clear_on_submit=True):
        pin = st.text_input("Enter PIN: (0000 for testing purposes)", type="password")
        submitted_pin = st.form_submit_button("Login")
        if submitted_pin:
            if pin == "0000":
                st.session_state.logged_in = True
                st.rerun() 
            else:
                st.error("Invalid PIN. Please try again.")
    st.stop() 

def generate_response(user_input):
    st.toast('Generating response')
    with st.spinner("Generating response", show_time=True):
        API_URL = "http://localhost:5000/api/predict"
        payload = [user_input,patient_id]
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                return data.get("message", "No message field found")
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception: {str(e)}"

st.set_page_config(page_title="MediHelp", layout="wide")

cols = st.columns([1, 10])
with cols[0]:
    if st.button("?", key="help_button"):
         st.session_state.show_help = True
with cols[1]:
    if st.button("Logout", key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.patient_info = None
        st.session_state.messages = []
        st.rerun()


if st.session_state.show_help:
    with st.container():
         st.markdown("<div class='help-container'><h3>Help</h3></div>", unsafe_allow_html=True)
         st.write(
             """
             **MediHelp Application Guide**
             
             - **Patient Information:** Enter a valid Patient ID to load the patient's details.
             - **Chat Interface:** Type your queries in the chat box and the assistant will respond.
             - **Clear Chat History:** Use the "Clear Chat History" button to reset your conversation.
             
             """
         )
         if st.button("Close Help", key="close_help"):
             st.session_state.show_help = False


st.markdown(
    """
    <style>
    body {
        background-color: rgb(0, 82, 245);
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
        color: black;
    }
    .user-bubble {
        background-color: #DCF8C6;
        align-self: flex-end;
        text-align: right;
    }
    .bot-bubble {
        background-color: rgb(255, 255, 255);
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
         patient_id = st.text_input("Enter Patient ID: (for testing purposes, valid ID ranges are 1-999)")
    submitted_patient = st.form_submit_button("Submit Patient ID")

if submitted_patient and patient_id:
    try:
        patient_name = patientDB.loc[patientDB['Patient ID'] == int(patient_id), 'Name'].values[0]
        patient_age = patientDB.loc[patientDB['Patient ID'] == int(patient_id), 'Age'].values[0]
        st.session_state.patient_info = {"id": patient_id, "name": patient_name, "age": patient_age}
    except Exception as e:
        st.error(f"Error: Invalid Patient ID.")
        st.session_state.patient_info = None

if st.session_state.patient_info:
    col1, col2 = st.columns(2)
    with col1:
         st.markdown(f"Patient Name: {st.session_state.patient_info['name']}</p>", unsafe_allow_html=True)
    with col2:
         st.markdown(f"Patient Age: {st.session_state.patient_info['age']}</p>", unsafe_allow_html=True)

if st.button("Clear Chat History"):
    st.session_state.messages = []

if st.session_state.patient_info:
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
else:
    st.info("Please enter a valid Patient ID to access the chat interface.")