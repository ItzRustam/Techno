"""This File Contains Important tools for Techno"""
"""TOOLs:
* web_search with ddgs
* read_file
* create_file
* find_file
"""

from pydantic import BaseModel
from typing import Dict, Any, Tuple
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.tools import tool
from ddgs import DDGS
import requests as rq
import wikipediaapi

import sys
from pathlib import Path

# Isolation for Techno
WORKSPACE = Path("./agent_workspace")
WORKSPACE.mkdir(exist_ok=True)

class APIResult(BaseModel):
    status: str
    summary: str
    api_result: Dict[Any, Any]


# output parser
parser = PydanticOutputParser(pydantic_object=APIResult)


@tool
def search_wikipedia(topic : str) -> str:
    """Search Wikipedia on given Topic. use only when user asked specific for wikipedia."""
    try:
        wiki = wikipediaapi.Wikipedia(
            user_agent="RSRoute-Agent Techno https://github.com/ItzRustam/Techno", 
            language="en"
        )

        page = wiki.page(topic)

        if page.exists():
            return str(page.text) # make sure for str object only.
        else:
            return f"No result found for {topic}"

    except Exception as E:
        return str(E)

@tool
def call_api(url : str, Data : dict, method : str = "get") -> Tuple[int, Dict[Any, Any]]:
    """
    Send an HTTP request to the specified API URL with the provided data.

    Args:
        url: The URL of the API endpoint to call.
        Data: Query parameters or request data to send with the request.
            Do not include keys whose values are None or NULL. Remove
            those keys from the dictionary before making the request.
        method: HTTP method to use. Supported methods are "get" and "post".
            Defaults to "get".

    Returns:
        A tuple containing the HTTP status code and the API response as a
        dictionary.

    Notes:
        Returns an error message when the request fails or an unsupported
        HTTP method is provided.
    """

    
    if method == "get":
        try:
            response = rq.get(url=url, params=Data)
            return response.status_code, response.json()
        except Exception as E:
            return response.status_code, {"Error": str(E)}
    elif method == "post":
        try:
            response = rq.post(url=url, params=Data)
            return response.status_code, response.json()
        except Exception as E:
            return response.status_code, {"Error": str(E)}
    else:
        return "Unsupported Method, Tool only supports `get`, `post`"

@tool
def find_file(filename : str) -> bool:
    """find file in agent workspace, returns True if file exists else returns False"""
    file_path = WORKSPACE / filename

    if file_path.exists():
        return True
    else:
        return False

@tool
def read_file(filename: str) -> str:
    """Read and return the contents of a file inside the agent workspace."""

    path = WORKSPACE / filename

    if not path.exists():
        return f"File not found: {filename}"

    if not path.is_file():
        return f"Not a file: {filename}"

    return path.read_text(encoding="utf-8")

@tool
def create_file(filename: str, content: str) -> str:
    """Create a text file inside the agent workspace.

    filename: Relative path such as hello.py.
    content: Complete text content to write into the file.
    """

    path = WORKSPACE / filename

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return f"Created file: {path}"

@tool
def web_search(query: str, max_result=5) -> str:
    """Search the web using DuckDuckGo and return relevant search results."""

    try:

        results = DDGS().text(
            query,
            max_results=max_result
        )

        if not results:
            return "No search results found."

        return "\n\n".join(
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('href', '')}\n"
            f"Snippet: {result.get('body', '')}"
            for result in results
        )
    except Exception as E:
        return str(E)
