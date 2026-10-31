import streamlit as st
from langgraph_backend import get_chatbot
from langchain_core.messages import HumanMessage
CONFIG={'configurable':{'thread_id':'1'}}

if 'messages' not in st.session_state:
     st.session_state['messages']=[]

if 'chatbot' not in st.session_state:
     st.session_state['chatbot']=get_chatbot()

# messages=[{'role':'user','content':'Hii'},
#           {'role':'ai','content':'How Can I Assist You'}]

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
    
# with st.chat_message('ai'):
#     st.text('Good Morning')