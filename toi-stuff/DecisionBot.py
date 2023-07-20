from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def need_agent(prompt):
    llm = AzureChatOpenAI(deployment_name="gpt35-team-3-0301", temperature=0)
    context = SystemMessage(
        content=f"""
        write context here and answer YES if the prompt needs an agent, and NO otherwise
        """
    )
    answer = llm(messages=[context, HumanMessage(content=prompt)])
    return (answer.content == "YES")