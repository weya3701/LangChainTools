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


if __name__ == "__main__":

    load_dotenv()
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

    print(
        "你好！我是您的開發助理。請告訴我您想做什麼？(輸入 exit 退出)"
    )

    generated_yaml_steps = []

    while True:
        user_input = input("指令 > ")
        if user_input.lower() == 'exit':
            break

        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": []
        })

        print("\n助理回應:")
        print(response['output'])
