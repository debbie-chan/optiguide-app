import streamlit as st

from optiguide_helper import init_optiguide, get_response


# Sidebar configuration for OpenAI API key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Setting up the main title and caption for the chatbot interface
st.title("💬 Economic Lotsizing Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLMs and OptiGuide")

# Managing el_messages using session state - initializing with a default assistant message
if "el_messages" not in st.session_state:
    st.session_state["el_messages"] = [{"role": "assistant", 
                                     "content": "I can help answer economic lotsizing questions. How can I help you today?"}]

# Displaying existing el_messages in the chat interface
for msg in st.session_state.el_messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handling user input in the chat interface
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()   # Stop execution if no API key is provided

    # Initializing OptiGuide
    agent, user = init_optiguide(openai_api_key, 
                                 "Economic Lotsizing",
                                 'models/economic_lotsizing.py')
    
    # Adding user's message to session state and displaying it in the chat interface
    st.session_state.el_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Getting a response from OptiGuide based on the user's input
    with st.spinner("Calculating..."):
        msg = get_response(user, agent, prompt)
    
    # Adding assistant's response to session state and displaying it in the chat interface
    st.session_state.el_messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

