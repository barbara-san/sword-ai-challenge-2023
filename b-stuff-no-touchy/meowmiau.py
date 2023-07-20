import os
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

AZURE_OPENAI_KEY = "4f8e9d40be39474c96fa1327dbd47516"
AZURE_OPENAI_ENDPOINT = "https://openai-resource-team-3-france.openai.azure.com/"
OPENAI_API_VERSION = "2023-03-15-preview"

os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_KEY
os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_ENDPOINT
os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
os.environ["OPENAI_API_TYPE"] = "azure"

''' chatgpt = AzureChatOpenAI(deployment_name="gpt35-team-3-0301")

input_text = "How to be happy?"
output_text = chatgpt([HumanMessage(content=input_text)]).content '''


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text="", display_method='markdown'):
        self.container = container
        self.text = initial_text
        self.display_method = display_method

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token + "/"
        display_function = getattr(self.container, self.display_method, None)
        if display_function is not None:
            display_function(self.text)
        else:
            raise ValueError(f"Invalid display_method: {self.display_method}")

query = st.text_input("input your query", value="Tell me a joke")
ask_button = st.button("ask")

st.markdown("### streaming box")
chat_box = st.empty()
stream_handler = StreamHandler(chat_box, display_method='write')
chat = AzureChatOpenAI(max_tokens=100, streaming=True, callbacks=[stream_handler])

st.markdown("### together box")

if query and ask_button:
    response = chat([HumanMessage(content=query)])
    llm_response = response.content
    st.markdown(llm_response)