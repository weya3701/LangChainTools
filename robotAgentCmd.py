import sys
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
    prompt = sys.argv[1]
    print("prompt: ", prompt)

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

    try:
        response = agent_executor.invoke({
            "input": prompt,
            "chat_history": []
        })

        print({
            "rsp": response['output']
        })
    except Exception as e:
        print({
            "rsp": e
        })
