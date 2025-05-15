


import sys
import os
import streamlit as st
import uuid
import html
import textwrap 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agent.parking_agent import ParkingAgent 

st.set_page_config(page_title="Parking AI Assistant", layout="centered", initial_sidebar_state="collapsed")

def load_css_and_fonts(css_file_path):
    st.markdown("<link href='https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap' rel='stylesheet'>", unsafe_allow_html=True)
    try:
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_file_path}. Ensure it's in the correct path relative to where Streamlit is run.")

css_file_path = os.path.join(os.path.dirname(__file__), "style.css")
load_css_and_fonts(css_file_path)


USER_AVATAR = "👤"
BOT_AVATAR = "🚗"

st.markdown(
    textwrap.dedent("""
        <div class="custom-header">
            <span class="header-icon">{}</span> Parking AI Assistant
        </div>
    """).format(BOT_AVATAR).strip(), 
    unsafe_allow_html=True
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Parking Assistant. How can I help you find or book a parking spot today?\nFor example, you can ask:\n* Find parking near Eiffel Tower for tomorrow.\n* What are the rates for Lot A?"}
    ]
if "parking_agent_initialized" not in st.session_state:
    st.session_state.parking_agent_initialized = False

if not st.session_state.parking_agent_initialized:
    try:
        from dotenv import load_dotenv
        dotenv_path = os.path.join(PROJECT_ROOT, ".env")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            print(f"UI: Loaded .env file from {dotenv_path}")
        else:
            print(f"UI: .env file not found at {dotenv_path}. Agent might fail if API keys are not set.")

        st.session_state.parking_agent = ParkingAgent(session_id=st.session_state.session_id)
        st.session_state.parking_agent_initialized = True
        print(f"UI: ParkingAgent initialized for session {st.session_state.session_id}")
    except Exception as e:
        st.error(f"Fatal Error: Failed to initialize Parking Agent. Check API keys and backend services. Error: {e}")
        st.stop()


chat_placeholder = st.empty()

def display_messages():
    """Renders the chat messages into the chat_placeholder."""
    message_html_list = ["<div class='chat-container' id='chat-area'>"] 

    for message_data in st.session_state.messages:
        avatar = USER_AVATAR if message_data["role"] == "user" else BOT_AVATAR
        message_class = "user-message" if message_data["role"] == "user" else "assistant-message"
        
        raw_content = message_data["content"]

        processed_content = html.escape(raw_content).replace("\n", "<br />\n")
        
        bubble_template = f"""
            <div class="message-bubble {message_class}">
                <span class="icon">{avatar}</span>
                <div class="message-content">
                    {processed_content}
                </div>
            </div>
            """

        html_bubble = textwrap.dedent(bubble_template).strip()
        message_html_list.append(html_bubble)
    

    scroll_script_html = textwrap.dedent("""
    <script>
        (function() {
            const chatArea = document.getElementById('chat-area');
            if (chatArea) {
                setTimeout(function() { // Small delay for content rendering
                    chatArea.scrollTop = chatArea.scrollHeight;
                }, 50);
            }
        })();
    </script>
    """).strip()

    message_html_list.append(scroll_script_html) 
    message_html_list.append("</div>") 
    full_html_chat = "".join(message_html_list)
    
    chat_placeholder.markdown(full_html_chat, unsafe_allow_html=True)


display_messages()


with st.container(): 
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_input_val = st.text_input(
            "Type your message...", 
            placeholder="Type your message here and press Enter or click Send", 
            label_visibility="collapsed",
            key="user_text_input_field"
        )
        submit_button = st.form_submit_button(label="Send")

if submit_button and user_input_val:
    st.session_state.messages.append({"role": "user", "content": user_input_val})

    if not st.session_state.get("parking_agent_initialized") or not hasattr(st.session_state, 'parking_agent'):
        st.error("Agent not available. Please refresh or check logs.")
        st.session_state.messages.append({"role": "assistant", "content": "Error: Agent is not available at the moment."})
    else:
        with st.spinner("Assistant is thinking..."):
            try:

                agent_response = st.session_state.parking_agent.invoke_agent(user_input_val)
                st.session_state.messages.append({"role": "assistant", "content": agent_response})
            except Exception as e:
                print(f"UI: Error invoking agent: {e}") 
                error_snippet = str(e)[:150] 
                user_friendly_error = f"Sorry, I encountered an issue processing your request. (Details: {error_snippet}...)"
                st.session_state.messages.append({"role": "assistant", "content": user_friendly_error})
    
    st.rerun()