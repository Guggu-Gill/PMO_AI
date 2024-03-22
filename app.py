from unittest import loader
import matplotlib
matplotlib.use('Agg') 
import streamlit as st

from embedchain import App
import queue
import threading
from io import StringIO
from PIL import Image
import os
import requests

from embedchain import App
from embedchain.config import BaseLlmConfig
from embedchain.helpers.callbacks import (StreamingStdOutCallbackHandlerYield,
                                          generate)
from web_page import WebPageLoader
import json
# os.environ["OPENAI_API_KEY"]=""

def read_json(name):
    file_path = name
    with open(file_path, 'r') as json_file:
        python_array = json.load(json_file)
        return python_array



pmo_links=read_json("pmo_links.json")

mann_ki_baat=read_json("mann-ki-baat.json")

@st.cache_resource
def modiJi():
    app=App()
    return app



@st.cache_resource
def add_data(arr_of_links,type):
    n=len(arr_of_links)
    for i in range(n):
        try:
            app.add(arr_of_links[i],data_type=type,loader=WebPageLoader())
        except Exception as e:
            print("Exception occurred:", e)  #
            print("missed",i,arr_of_links[i])


app=modiJi()

assistant_avatar_url="modiJiWithTurban.png"
modiji_avatar="modiJiWithTurban.png"

#adding 3000 pmo links
add_data(arr_of_links=pmo_links, type="web_page")




st.markdown("<h1 style='text-align: center; color: #aaa;'>PM OFFICE AI 🇮🇳</h1>", unsafe_allow_html=True)

styled_caption = '<p style="font-size: 18px; color: #aaa;">🇮🇳 Made by <a href="https://www.linkedin.com/in/basantsingh1000/">Basant Singh</a> powered by <a href="https://github.com/embedchain/embedchain">Embedchain</a></p>'  # noqa: E501
st.markdown(styled_caption, unsafe_allow_html=True)  
st.markdown('<p style="font-size: 10px; color: #aaa;">not associated with PM OFFICE🇮🇳 or BJP🪷</p>',unsafe_allow_html=True)

#copied from streamlit community
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(modiji_avatar)



 



if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
Hi, I am PM OFFICE AI on duty of Prime Minister of India🇮🇳.
I source knowlege from non-political PMO website but as an AI model I can hallucinate, Always rely on Govt Of India🇮🇳 expert.
\n

""",

        }
    ]



prompt_for_llm = """
You are AI assistant tasked to answer questions based on context only. 

### If its outside context answer "Outside Context."
### answer should be not too lengthy.

Context information:
----------------------
$context
----------------------

Query: $query
Answer:
"""

for message in st.session_state.messages:
    role=message['role']
    with st.chat_message(role,avatar=assistant_avatar_url if role == "assistant" else None):
        st.markdown(message["content"])


if prompt := st.chat_input("Pls ask one question at a time. "):
    
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant",avatar=assistant_avatar_url):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""
        q = queue.Queue()


        def app_response(result):
            config = BaseLlmConfig(prompt=prompt_for_llm,stream=True, callbacks=[StreamingStdOutCallbackHandlerYield(q)])
            answer, citations = app.chat(prompt, config=config, citations=True)
            result["answer"] = answer
            result["citations"] = citations


        #this code produces streaming output using threads, logic might be different in other frameorks like langchain
        results = {}
        thread = threading.Thread(target=app_response, args=(results,))
        thread.start()
        for answer_chunk in generate(q):
            full_response += answer_chunk
            msg_placeholder.markdown(full_response)
        
        
        thread.join()


        answer, citations = results["answer"], results["citations"]
        if citations:
            full_response += "\n\n**Sources**:\n"
            sources = list(set(map(lambda x: x[1]["url"], citations)))
            for i, source in enumerate(sources):
                full_response += f"{i+1}. {source}\n"

        msg_placeholder.markdown(full_response)


        st.session_state.messages.append({"role": "assistant", "content": full_response})
    









