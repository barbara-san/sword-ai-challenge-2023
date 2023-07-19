import os
import langchain
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

AZURE_OPENAI_KEY = "4f8e9d40be39474c96fa1327dbd47516"
AZURE_OPENAI_ENDPOINT = "https://openai-resource-team-3-france.openai.azure.com/"
OPENAI_API_VERSION = "2023-03-15-preview"

os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_KEY
os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_ENDPOINT
os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
os.environ["OPENAI_API_TYPE"] = "azure"

chatgpt = AzureChatOpenAI(deployment_name="gpt35-team-3-0301")
text = "How to be happy?"
print(chatgpt([HumanMessage(content=text)]).content)

from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory, CombinedMemory, ConversationSummaryMemory

conv_memory = ConversationBufferWindowMemory(
    memory_key="chat_history_lines",
    input_key="input",
    k=1
)

summary_memory = ConversationSummaryMemory(llm=chatgpt, input_key="input")
# Combined
memory = CombinedMemory(memories=[conv_memory, summary_memory])
_DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Summary of conversation:
{history}
Current conversation:
{chat_history_lines}
Human: {input}
AI:"""
PROMPT = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines"], template=_DEFAULT_TEMPLATE
)

conversation = ConversationChain(
    llm=chatgpt, 
    verbose=False, 
    memory=memory,
    prompt=PROMPT
)

print("\n")

print(conversation.run("what is 2+2?"))
print(conversation.run("What was this conversation about?"))
print(conversation.run("Tell me a joke about this conversation topic"))