from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
import ast
from assignment_chat.main import get_graph
import gradio as gr
from dotenv import load_dotenv
import os

from utils.logger import get_logger

_logs = get_logger(__name__)

llm = get_graph()

load_dotenv('.secrets')

# Helper function to output full lyrics from lyrics API call tool
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

def assignment_chat(message: str, history: list[dict]) -> str:
    langchain_messages = []
    n = 0
    _logs.debug(f"History: {history}")
    for msg in history:
        if msg['role'] == 'user':
            langchain_messages.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            langchain_messages.append(AIMessage(content=msg['content']))
            n += 1
    langchain_messages.append(HumanMessage(content=message))

    state = {
        "messages": langchain_messages,
        "llm_calls": n
    }

    response = llm.invoke(state)
    return response['messages'][len(response['messages']) - 1].content

chat = gr.ChatInterface(
    fn=assignment_chat
)

if __name__ == "__main__":
    _logs.info('Starting Music Chat App...')
    chat.launch()
