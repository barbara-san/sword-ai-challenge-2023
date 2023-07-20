import os
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory, CombinedMemory, ConversationSummaryMemory

AZURE_OPENAI_KEY = "4f8e9d40be39474c96fa1327dbd47516"
AZURE_OPENAI_ENDPOINT = "https://openai-resource-team-3-france.openai.azure.com/"
OPENAI_API_VERSION = "2023-03-15-preview"

os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_KEY
os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_ENDPOINT
os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
os.environ["OPENAI_API_TYPE"] = "azure"

math_llm = AzureChatOpenAI(deployment_name="gpt35-team-3-0301", max_tokens=100, temperature=0.2)
summary_llm = AzureChatOpenAI(deployment_name="gpt35-team-3-0301")

# Trying to create a base pre-prompt for math
context = """\
The following text is simply an guide that the AI must follow after receiving this text input. \
The AI MUST asnwer to this prompt with \"Understood!\" and nothing else, as it only exists to give context to the AI. \
This is a friendly conversation between a human and an AI. \
The AI serves the purpose of being a mathematics tutor. \
The human is considered to be a highschooler learning in the Portuguese schools, which follow the portuguese teaching system. \
The AI should help the human by giving clear detail on how to solve an exercise or how to understand a concept. \
The AI must not use techniques that are considered to be of higher educational experience. \
Any equations provided by the AI should be written delimited by ```. \
If the AI does not know the answer to a question, it truthfully says it does not know. \
"""

conv_memory = ConversationBufferWindowMemory(
    memory_key="chat_history_lines",
    input_key="input",
    k=1
)

summary_memory = ConversationSummaryMemory(llm=summary_llm, input_key="input")
# Combined
memory = CombinedMemory(memories=[conv_memory, summary_memory])

_DEFAULT_TEMPLATE = f"{context}" + """

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
    llm=math_llm, 
    verbose=False, # change to False to only show the answer when running
    memory=memory,
    prompt=PROMPT
)

print(conversation.run(context))

from PerfectPrompt import better_prompt

while True:
    input_prompt = input()
    if input_prompt == "X":
        break
    new_input_prompt = better_prompt(input_prompt)
    print(f"\nOriginal input:\n{input_prompt}\n\"Better\" input:\n{new_input_prompt}")
    answer = conversation.run(new_input_prompt)
    print(f"Conversation bot output:\n\t{answer}\n")

