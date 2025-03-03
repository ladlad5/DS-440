import streamlit as st

if 'messages' not in st.session_state:
    st.session_state.messages = []

def generate_response(user_input):
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
