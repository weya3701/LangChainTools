import os
from langchain.tools import tool
from models.utils.interactive import GenAI


@tool(description="直接對AI模型發問的工具，直接輸入prompt即可獲得回覆")
def get_ai_content(command: str) -> str:

    genai = GenAI(
        api_key=os.getenv("API_KEY"),
        cht_model=os.getenv("AIModel")
    )
    return genai.gen_content(command)
