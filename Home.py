import streamlit as st

from optiguide_helper import init_optiguide, get_response


# Sidebar configuration for OpenAI API key input
with st.sidebar:
    st.write("Choose one of the models above ⬆️")

# Setting up the main title and caption for the chatbot interface
st.title("💬 OptiGuide Chatbots")
st.caption("🚀 A collection of streamlit chatbot powered by OpenAI LLMs and OptiGuide")

st.markdown('''
            This demo application showcases the following models:  
            1. Economic Lotsizing
            2. Safety Stock
            3. Supply Network

            Pick one of the models in the sidebar to ask the chatbot questions!
            ''')