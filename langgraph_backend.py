from langgraph.graph import StateGraph,START,END
from langchain_openai  import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict,Annotated
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage


load_dotenv()


llm = ChatOpenAI(model= 'gpt-4o')

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':[response]}


def get_chatbot():
    graph=StateGraph(ChatState)

    # Add Nodes
    graph.add_node('chat_node',chat_node)

    # Add Edges
    graph.add_edge(START,'chat_node')
    graph.add_edge('chat_node',END)

    checkpointer=InMemorySaver()

    chatbot=graph.compile(checkpointer=checkpointer)

    return chatbot

# chatbot=get_chatbot()
# config={'configurable':{'thread_id':'1'}}
# response=chatbot.invoke({'messages':[HumanMessage(content='which one is the biggest bird in size who can fly')]},config=config)
# print(response)

# print("************************************************************************")

# print(chatbot.get_state(config).values['messages'])

# print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

# print(chatbot.get_state(config).values['messages'][0].content)