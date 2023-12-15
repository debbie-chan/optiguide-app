import streamlit as st

from optiguide_helper import init_optiguide, get_response


# Sidebar configuration for OpenAI API key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Setting up the main title and caption for the chatbot interface
st.title("💬 Supply Network Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLMs and OptiGuide")

# Managing sn_messages using session state - initializing with a default assistant message
if "sn_messages" not in st.session_state:
    st.session_state["sn_messages"] = [{"role": "assistant", 
                                     "content": "I can help answer supply network questions. How can I help you today?"}]

# Displaying existing sn_messages in the chat interface
for msg in st.session_state.sn_messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handling user input in the chat interface
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()   # Stop execution if no API key is provided

    # Initializing OptiGuide
    agent, user = init_optiguide(openai_api_key, 
                                 "Supply Network",
                                 'models/supply_network.py', 
                                 'models/icl_examples/icl_supply_network.py')
    
    # Adding user's message to session state and displaying it in the chat interface
    st.session_state.sn_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Getting a response from OptiGuide based on the user's input
    with st.spinner("Calculating..."):
        msg = get_response(user, agent, prompt)
    
    # Adding assistant's response to session state and displaying it in the chat interface
    st.session_state.sn_messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

