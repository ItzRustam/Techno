from techno.tools import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama # Local Only. Not Ideal
from dotenv import load_dotenv
from rich import print as rprint
from techno.prompt import system_message
import os
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

tools_name = {
    "web_search": web_search,
    "create_file": create_file,
    "read_file": read_file,
    'find_file': find_file,
    "call_api": call_api
}


MAX_TOOL_USE = int(os.getenv("MAX_TOOL_USE"))

def create_agent():

    llm = ChatGoogleGenerativeAI(model=os.getenv("MODEL"))

    tools = [web_search, create_file, read_file, find_file, call_api]

    # Agent
    Agent = llm.bind_tools(tools=tools)

    return Agent

def run_agent():
    rprint("[red]Techno is Here[/red]")

    message = []
    message.append(system_message)

    llm_with_tool = create_agent()

    while True:
        userInput = input("You: ")

        if userInput.lower() == "exit":
            break

        query = HumanMessage(content=userInput)
        message.append(query)

        result = llm_with_tool.invoke(message)
        message.append(result)

        tool_used = 0

        while result.tool_calls:
            if tool_used > MAX_TOOL_USE:
                print(
                    "Error: Too Many Tools Called, "
                    "set MAX_TOOL_USE more than 10."
                )
                return 1 # Error Code

            tool_call_info = result.tool_calls[0]

            rprint("Current Tool: ", tool_call_info)

            chosen_tool = tools_name[tool_call_info["name"]]

            tool_result = chosen_tool.invoke(
                tool_call_info["args"]
            )

            tool_message = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call_info["id"],
            )

            message.append(tool_message)

            result = llm_with_tool.invoke(message)
            message.append(result)

            tool_used += 1

        response = parser.invoke(result)

        rprint(response)
        rprint(f"Called: {tool_used} tools.")

