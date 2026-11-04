import streamlit as st
from langgraph_backend import get_chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid



st.markdown("""
    <style>
    div.stButton > button {
        background: transparent;
        border: none;
        padding: 0;
        color: inherit;
        text-align: left;
        box-shadow: none;
        font-size: 14px;
        width: 100%;
    }

    div.stButton > button:hover {
        background: transparent;
        border: none;
        color: #4A90E2;
        text-decoration: underline;
    }

    div.stButton > button:focus {
        outline: none;
        box-shadow: none;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)


# def show_conversations():
#      print(st.session_state['thread_ids'])
#      for thread in st.session_state['thread_ids']:
#         thread_id, label = thread.values()
#         print(f"THREAD_ID : {thread_id}")
#         print(f"LABEL : {label}")
#         if label is not None:
#             if st.sidebar.button(get_label_formated(label)):
#                 st.session_state['thread_id']=thread_id
#                 messages=load_conversations(thread_id=thread_id)
#                 temp_history=[]
#                 for msg in messages:
#                     if isinstance(msg,HumanMessage):
#                             role='user'
#                     else :
#                         role='ai'
#                     temp_history.append({'role':role,'content':msg.content})
#                 st.session_state['messages']=temp_history


def show_conversations():
    for thread in st.session_state['thread_ids']:
        print(thread)
        thread_id, label = thread.values()

        if label is not None:
            if st.sidebar.button(
                get_label_formated(label),
                key=f"thread_{thread_id}"
            ):
                st.session_state['thread_id'] = thread_id

                messages = load_conversations(thread_id=thread_id)

                temp_history = []
                for msg in messages:
                    role = 'user' if isinstance(msg, HumanMessage) else 'ai'
                    temp_history.append({
                        'role': role,
                        'content': msg.content
                    })

                st.session_state['messages'] = temp_history

# def validate_thread_id(thread_id):
#     return any(
#         thread["thread_id"] == thread_id
#         for thread in st.session_state['thread_ids']
#     )

def validate_thread_id(thread_id):
    return any(
        thread["thread_id"] == thread_id and thread["label"] is not None
        for thread in st.session_state["thread_ids"]
    )
     

def update_thread_id():
     new_thread_id=generate_thread_id()
     st.session_state['thread_id']=new_thread_id
     st.session_state['thread_ids'].append({'thread_id':new_thread_id,'label':None})
     

def reset_messages():
     st.session_state['messages']=[]

def load_conversations(thread_id):
     config={'configurable':{'thread_id':thread_id}}
     return st.session_state['chatbot'].get_state(config=config).values['messages']


def get_label_formated(label):
     return label[:35] + "..." if len(label) > 35 else label


def add_thread_id(label):
     st.session_state['thread_ids'].append({'thread_id':st.session_state['thread_id'],'label':str(label)})


def generate_thread_id():
     return uuid.uuid4()

if 'messages' not in st.session_state:
     st.session_state['messages']=[]

if 'chatbot' not in st.session_state:
     st.session_state['chatbot']=get_chatbot()


if 'thread_id' not in st.session_state:
     st.session_state['thread_id']= generate_thread_id()


if 'thread_ids' not in st.session_state:
     st.session_state['thread_ids']=retrieve_all_threads(st.session_state['chatbot'])
     
    #  st.session_state['thread_ids'].append(str(st.session_state['thread_id']))




# if 'thread_ids' not in st.session_state:
#      st.session_state['thread_ids']=[]

# messages=[{'role':'user','content':'Hii'},
#           {'role':'ai','content':'How Can I Assist You'}]

# CONFIG={'configurable':{'thread_id':st.session_state['thread_id']}}
CONFIG={'configurable':{'thread_id':st.session_state['thread_id']},
        'metadata':{'thread_id':st.session_state['thread_id']},
        'run_name':'chat_node'}



# ********************************** Sidebar UI *************************************************

st.sidebar.title("Langgraph Chatbot")

if st.sidebar.button("New Chat"):
     update_thread_id()
     reset_messages()
     

st.sidebar.header("MY CONVERSATIONS")

# st.sidebar.button(st.session_state['thread_id'])

# for thread_id in st.session_state['thread_ids']:
#      if st.sidebar.button(thread_id):
#         st.session_state['thread_id']=thread_id
#         messages=load_conversations(thread_id=thread_id)
#         temp_history=[]
#         for msg in messages:
#             if isinstance(msg,HumanMessage):
#                     role='user'
#             else :
#                  role='ai'
#             temp_history.append({'role':role,'content':msg.content})
#         st.session_state['messages']=temp_history


# for thread_id,label in st.session_state['thread_ids']:
#      if st.sidebar.button(get_label_formated(label)):
#         st.session_state['thread_id']=thread_id
#         messages=load_conversations(thread_id=thread_id)
#         temp_history=[]
#         for msg in messages:
#             if isinstance(msg,HumanMessage):
#                     role='user'
#             else :
#                  role='ai'
#             temp_history.append({'role':role,'content':msg.content})
#         st.session_state['messages']=temp_history

show_conversations()





for message in st.session_state['messages']:
    # print(item)
    with st.chat_message(message['role']):
        st.text(message['content'])




user_input = st.chat_input('Type Here ......')

if user_input:
    new_message={'role':'user','content':user_input}

    st.session_state['messages'].append(new_message)

    with st.chat_message('human'):
            st.text(user_input)

    # response=st.session_state['chatbot'].invoke({'messages':[HumanMessage(content=user_input)]},config=CONFIG)

    # ai_message={'role':'ai','content':response['messages'][-1].content}
    # st.session_state['messages'].append(ai_message)

    # with st.chat_message('ai'):
    #             st.text(ai_message['content'])

    # for message_chunk,metadata in st.session_state['chatbot'].stream({'messages':[HumanMessage(content=user_input)]},config=CONFIG,stream_mode='messages'):
    #       print(message_chunk)
    #       print("==========")
    #       print(metadata)

    with st.chat_message('ai'):
          ai_message=st.write_stream(message_chunk.content for message_chunk,metadata in st.session_state['chatbot'].stream({'messages':[HumanMessage(content=user_input)]},config=CONFIG,stream_mode='messages'))
          st.session_state['messages'].append({'role':'ai','content':ai_message})

          if not validate_thread_id(st.session_state['thread_id']):
            #    print("INVOKED")
               st.toast("INVOKED!", icon="✅")
               print("THREAD IDS : ")
               print(st.session_state['thread_ids'])
               add_thread_id(user_input)
            #    show_conversations()
    
# with st.chat_message('ai'):
#     st.text('Good Morning')


