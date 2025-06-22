from langchain_openai import AzureChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0
)

def get_agent(df: pd.DataFrame):
    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type="openai-tools",
        allow_dangerous_code=True
    )
