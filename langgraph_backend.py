from langgraph.graph import StateGraph,START,END
from langchain_openai  import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict,Annotated
import operator
import requests
from pathlib import Path
from langgraph.prebuilt.tool_node import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
import sqlite3
from pathlib import Path
import os


load_dotenv()

WEATHER_API= os.getenv('WEATHER_API')




## Define Tools
@tool('calculator_tool')
def calculator_tool(first_number : float, second_number : float,operation : str):
    """Performs basic arithmetic calculations on two numerical inputs. Accepts first_number, second_number, and an operation as arguments and returns the calculated result.
    Supported operations:
    addition: Adds the two numbers.
    subtraction: Subtracts the second number from the first number.
    multiplication: Multiplies the two numbers.
    division: Divides the first number by the second number.
    Use this tool whenever a mathematical calculation involving these four operations is required. Ensure that the operation is one of the supported operations and that the second number is not zero when performing division."""

    if operation.lower() == 'addition':
        result=first_number+second_number
        return {'first_number':first_number,'second_number':second_number,'operation':operation,'result':result} 
    elif operation.lower() == 'subtraction':
        result=first_number-second_number
        return {'first_number':first_number,'second_number':second_number,'operation':operation,'result':result} 
    elif operation.lower() == 'multiplication':
        result=first_number*second_number
        return {'first_number':first_number,'second_number':second_number,'operation':operation,'result':result} 
    elif operation.lower() == 'division':
        result=first_number/second_number
        return {'first_number':first_number,'second_number':second_number,'operation':operation,'result':result} 
    else : 
        return {'Error':'Invalid Operation'}

@tool('get_weather_data')
def get_weather_data(city:str):
    """Fetches the current weather information for a specified city using the Weatherstack API.
    Accepts a city name as input and retrieves the latest available weather data for that location. Returns relevant weather information, such as temperature and other available weather conditions.
    Use this tool whenever the user asks about the current weather or temperature of a specific city. Always provide a valid city name to retrieve location-specific weather information."""
    
    response = requests.get(f"{WEATHER_API}{city}")
    return response.json()


search_tool = DuckDuckGoSearchRun()

tools=[search_tool,calculator_tool,get_weather_data]

llm = ChatOpenAI(model= 'gpt-4o')
llm_with_tools= llm.bind_tools(tools=tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm_with_tools.invoke(messages)
    return {'messages':[response]}


# def get_chatbot():
#     graph=StateGraph(ChatState)

#     # Add Nodes
#     graph.add_node('chat_node',chat_node)

#     # Add Edges
#     graph.add_edge(START,'chat_node')
#     graph.add_edge('chat_node',END)

#     # checkpointer=InMemorySaver()
#      # Initialize SQLite checkpointer
#     checkpointer_context = SqliteSaver.from_conn_string(
#         "checkpoints.sqlite"
#     )

#     checkpointer = checkpointer_context.__enter__()

#     chatbot=graph.compile(checkpointer=checkpointer)

#     return chatbot


# def retrieve_all_threads(chatbot):
#     all_threads = set()

#     for checkpoint in chatbot.checkpointer.list(None):
#         thread_id = checkpoint.config["configurable"]["thread_id"]
#         print(checkpoint)
#         all_threads.add(thread_id)

#     return sorted(all_threads)




def retrieve_all_threads(chatbot):
    threads = {}

    # SQLite returns checkpoints from newest to oldest.
    for checkpoint in chatbot.checkpointer.list(None):
        thread_id = checkpoint.config["configurable"]["thread_id"]

        if thread_id not in threads:
            threads[thread_id] = {
                "thread_id": thread_id,
                "label": None,
            }

        messages = checkpoint.checkpoint.get(
            "channel_values", {}
        ).get("messages", [])

        for message in messages:
            if isinstance(message, HumanMessage):
                threads[thread_id]["label"] = message.content
                break

    return [
        threads[thread_id]
        for thread_id in sorted(threads)
    ]



def get_chatbot():
    db_path = Path(__file__).resolve().with_name("checkpoints.sqlite")

    # Keep this connection open for the chatbot's lifetime.
    conn = sqlite3.connect(
        str(db_path),
        check_same_thread=False,
    )

    checkpointer = SqliteSaver(conn)

    tool_node=ToolNode(tools=tools)

    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)
    graph.add_node('tools',tool_node)
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges('chat_node',tools_condition)
    graph.add_edge('tools','chat_node')
    # graph.add_edge("chat_node", END)

    try:
        return graph.compile(checkpointer=checkpointer)
    except Exception:
        conn.close()
        raise


chatbot=get_chatbot()
config={'configurable':{'thread_id':'1'}}
response=chatbot.invoke({'messages':[HumanMessage(content='what is two multiply by four')]},config=config)
print(response)

# print(chatbot)

# retrieve_all_threads(chatbot)



