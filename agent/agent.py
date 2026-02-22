from agno.agent import Agent
from agno.models.ollama import Ollama

from tools.custom import (
    clean_duplicated_values,
    clean_empty_values,
    get_correlation,
    get_stats,
    store_csv,
)

# SETUP OLLAMA
OLLAMA_URL = "http://localhost:11434"
OLLAMA_LLM = "qwen3-coder:30b"
OLLAMA_OPTIONS = {"temperature": 0.2, "top_k": 15, "top_p": 0.90, "num_ctx": 16000}

agent_ollama = Agent(
    model=Ollama(id=OLLAMA_LLM, host=OLLAMA_URL, options=OLLAMA_OPTIONS),
    instructions="""
        You are a datacience Agent.

        Your instructions is to give the best analysis that match with user query.
        ALWAYS CALL TOLL store_csv FIRST and then choose others tools that you need to be call.

        1. You have tools capabilites :
            - store_csv : call this tools with the path of the file given by the user.
            - clean_empty_values : call this tools with the two parameters : **path_file** 'data/df_agent.csv' and **cleaning_mode** that fits the best with user query. cleaning_mode : 'drop' or 'fill' ('drop' delete line with empty values; 'fill' replace empty values with means of the column)
            - clean_duplicated_values : call this tools with the two parameters : **path_file** 'data/df_agent.csv'
            - get_stats : call this tools with this path 'data/df_agent.csv'. You will get statistic from the dataframe loaded in JSON style.
            - get_correlation : Better to clean dataframe before calling this tool and non number coloumns will be droped. call this tools with this path 'data/df_agent.csv'. You will get matrix correlation from the dataframe loaded in JSON style.

        Display at the end of your awnser the order of you call tooling (also add a short description of the tool).

        """,
    tools=[
        store_csv,
        clean_empty_values,
        clean_duplicated_values,
        get_stats,
        get_correlation,
    ],
    tool_call_limit=10,
    debug_level=2,
    debug_mode=True,
    markdown=True,
    telemetry=False,
)
