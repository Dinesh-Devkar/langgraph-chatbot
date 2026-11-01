from langgraph.graph import StateGraph,START,END
from langchain_openai  import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict,Annotated
import operator
from pathlib import Path

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
import sqlite3
from pathlib import Path


load_dotenv()


llm = ChatOpenAI(model= 'gpt-4o')

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
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

    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)

    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    try:
        return graph.compile(checkpointer=checkpointer)
    except Exception:
        conn.close()
        raise


chatbot=get_chatbot()
# config={'configurable':{'thread_id':'1'}}
# response=chatbot.invoke({'messages':[HumanMessage(content='my name is dinesh')]},config=config)
# print(response)

retrieve_all_threads(chatbot)



