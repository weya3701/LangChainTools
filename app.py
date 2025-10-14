# app.py
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# AI robot agent packages.
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
import os
from models.bot_tools import (
    get_simplified_dom, time_sleep, open_website,
    run_by_js, find_element_and_send_keys, find_element_and_click,
    get_test_case
)
from models.cmd_tools import (
    run_command, cat_command
)
from models.ai_tool import (
    get_ai_content
)
from dotenv import load_dotenv
from system.prompt.robot_prompt import system_prompt

# 載入環境變數
load_dotenv()
# 建立 Flask 應用程式實例
app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():

    prompt_data = request.data
    print(prompt_data)

    # Call AI robot agent.

    tools = [
        open_website, get_simplified_dom,
        find_element_and_send_keys, find_element_and_click,
        time_sleep, run_by_js,
        run_command, cat_command,
        get_ai_content, get_test_case
    ]

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("AIModel"),
        google_api_key=os.getenv("API_KEY")
    )

    optimized_prompt_basic = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, optimized_prompt_basic)

    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True
    )

    try:
        response = agent_executor.invoke({
            "input": prompt_data,
            "chat_history": []
        })

        return jsonify(
            {
                "code": 201,
                "status": "successed.",
                "response": response['output']
            }
        ), 201
    except Exception as e:

        return jsonify(
            {
                "code": 500,
                "status": "successed.",
                "response": e
            }
        ), 201


# --- 啟動應用程式 ---

if __name__ == '__main__':
    # host='0.0.0.0' 讓外部電腦可以連接
    # debug=True 讓程式碼變更後自動重啟，並提供詳細錯誤訊息
    app.run(host='0.0.0.0', port=5000, debug=True)
