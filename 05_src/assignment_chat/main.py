from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage,  HumanMessage, AIMessage, ToolMessage

from dotenv import load_dotenv
import json
import requests
import os
import ast

from assignment_chat.prompts import return_instructions
from assignment_chat.tools_lyrics import get_lyrics
from assignment_chat.tools_websearch import get_artist_history
from assignment_chat.tools_music import recommend_albums
from utils.logger import get_logger


_logs = get_logger(__name__)
load_dotenv(".env")
load_dotenv(".secrets")


chat_agent = init_chat_model(
    "openai:gpt-4o-mini",
)
tools = [get_lyrics, recommend_albums, get_artist_history]

instructions = return_instructions()


# Helper function to output full song lyrics
def extract_tool_result(messages, target_tool):
    """
    Searches the message log to see if target_tool variable is called. It will be "get_lyrics" tool. 
    If found, final message is outputed as tool message for full lyrics instead of final AI message.
    """
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for call in msg.tool_calls:
                if call["name"] == target_tool:
                    tool_call_id = call["id"]

                    for tool_msg in messages:
                        if (
                            isinstance(tool_msg, ToolMessage)
                            and tool_msg.tool_call_id == tool_call_id
                        ):
                            return tool_msg.content

    return None

# @traceable(run_type="llm")
def call_model(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    response = chat_agent.bind_tools(tools).invoke( [SystemMessage(content=instructions)] + state["messages"])

    # If lyric_tool is called, output full tool result instead of message passed through AI
    messages = response["messages"]
    lyrics_result = extract_tool_result(
        messages,
        "get_lyrics"
    )
        
    if lyrics_result:
        return lyrics_result
    
    return {
        "messages": [response]
    }

def get_graph():
    
    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    return graph

