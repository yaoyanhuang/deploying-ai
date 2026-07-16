import requests
from urllib.parse import quote
from langchain.tools import tool
import json
import getpass
import os

from utils.clients import get_client
client = get_client()

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")
    
from langchain_tavily import TavilySearch
from langchain.agents import create_agent

@tool
def get_artist_history(artist: str) -> str:
    """
    Uses a simple web search to return the history of a musical artist.
    """
    tavily_search_tool = TavilySearch(
        max_results = 5,
        topic = "general"
    )
    results = tavily_search_tool.invoke({"query": f"{artist} music artist history biography"})
    return results