from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from Config import load_environment
load_environment()

# You must also ask for the answer to be in a specific format, that best fits the question or request, for example, using bullet points or an ordered list. You MUST choose the formatation on your own. \

def perfect_prompt(prompt, memory):
    llm = AzureChatOpenAI(deployment_name="gpt35-team-3-0301", temperature=0)
    context = SystemMessage(
        content="""
            The AI is going to receive a prompt from the user, delimited by ```. \
            The AI must process the prompt and alter it in order to make it more accurate and understandable for any LLM model. \
            The context and idea of the given prompt MUST remain inaltered. \
            The new prompt may include new additional text that is predictable to be presented by the human in the future. \
            You MUST only return the new prompt, and nothing else.\
            """
    )
    #memory_and_prompt = 
    answer = llm(messages=[context, HumanMessage(content=prompt)])
    return answer.content