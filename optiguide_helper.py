import streamlit as st

# test Gurobi installation
import gurobipy as gp
from gurobipy import GRB
from eventlet.timeout import Timeout

# import auxillary packages
import requests  # for loading the example source code
import openai

# import flaml and autogen
from flaml import autogen
from flaml.autogen.agentchat import Agent, UserProxyAgent
from optiguide.optiguide import OptiGuideAgent

from io import StringIO
import sys

autogen.oai.ChatCompletion.start_logging()

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-4",
            "gpt4",
            "gpt-4-32k",
            "gpt-4-32k-0314",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0301",
            "chatgpt-35-turbo-0301",
            "gpt-35-turbo-v0301",
        }
    }
)

@st.cache_resource
def init_optiguide(api_key, source_code_link):
    openai.api_key = api_key

    # Get the source code
    code = open(source_code_link, "r").read()

    agent = OptiGuideAgent(
        name="OptiGuide Last Mile Problem",
        source_code=code,
        debug_times=1,
        example_qa="",
        llm_config={
            "request_timeout": 600,
            "seed": 42,
            "config_list": config_list,
        }
    )

    user = UserProxyAgent(
        "user", max_consecutive_auto_reply=0,
        human_input_mode="NEVER", code_execution_config=False
    )

    return agent, user

def get_response(user, agent, question):
    # Redirecting print output to a variable
    captured_output = StringIO()
    sys.stdout = captured_output

    user.initiate_chat(agent, message=question)

    # Resetting sys.stdout to the default value (console output)
    sys.stdout = sys.__stdout__

    # Extracting the captured output
    raw_output = captured_output.getvalue()
    with open('out.txt', 'w') as output:
        output.write(raw_output)
    response = raw_output.split('(to user):')[1].strip('-').strip()

    return response