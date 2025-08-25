import os
import requests
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.utilities import  WikipediaAPIWrapper
from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_google_community import GoogleSearchAPIWrapper

load_dotenv(override=True)

pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"


def push(text: str):
    if not pushover_token or not pushover_user:
        raise ValueError("PUSHOVER_TOKEN or PUSHOVER_USER not set in environment")
    requests.post(
        url=pushover_url,
        data={"token": pushover_token, "user": pushover_user, "message": text},
    )
    return "success"


def get_file_tools():
    os.makedirs("sendbox", exist_ok=True)
    toolkit = FileManagementToolkit(root_dir="sendbox")
    return toolkit.get_tools()


async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


async def tools_setup():

    serper = serper = GoogleSearchAPIWrapper(
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    google_cse_id=os.getenv("GOOGLE_CSE_ID")
)

    push_tool = Tool(
        name="send_push_notification",
        func=push,
        description="Send a push notification using Pushover",
    )

    search_tool = Tool(
        name="google_search",
        func=serper.run,
        description="Use this tool to perform web searches when external information is needed",
    )

    wikipedia = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)

    python_repl = PythonREPLTool()

    file_tools = get_file_tools()

    all_tools = [push_tool, search_tool, wiki_tool, python_repl] + file_tools

    return all_tools


    








