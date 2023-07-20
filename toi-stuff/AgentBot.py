from langchain.chat_models import AzureChatOpenAI
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper

def get_context(subject):
    return f"""\
    The following text is simply an guide that the AI must follow after receiving this text input. \
    You won't need to use tools to answer to this prompt, as it only exists to give context to the AI. \
    For any following prompt given you can use tools to achieve an answer.
    This is a friendly conversation between a human and an AI. \
    The AI serves the purpose of being a {subject} tutor. \
    The human is considered to be a highschooler learning in the Portuguese schools, which follow the portuguese teaching system. \
    The AI should help the human by giving clear detail on how to solve an exercise or how to understand a concept. \
    The AI must not use techniques that are considered to be of higher educational experience. \
    If the AI does not know the answer to a question, it truthfully says it does not know. \
    You have access to the following tools:\
    """

def get_tools(subject):
    # APIs
    wolframalpha = WolframAlphaAPIWrapper()
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    # tools map
    tools_of_subject = {
        "Mathematics" : [
            Tool(
                name="Math Helper",
                func=wolframalpha.run,
                description="useful for when you need to answer questions math related"
            )
        ],
        "History" : [
            Tool(
                name="Wikipedia Helper",
                func=wikipedia.run,
                description="useful for when you need to search about any topic and get some historical knowledge from it"
            )
        ]
    }

    return tools_of_subject.get(subject)

def get_prompt(subject):
    suffix = """Begin!"

    {chat_history}
    Question: {input}
    {agent_scratchpad}"""

    return ZeroShotAgent.create_prompt(
        get_tools(subject),
        prefix=get_context(subject),
        suffix=suffix,
        input_variables=["input", "chat_history", "agent_scratchpad"],
    )


class AgentChatBot:
    def __init__(self, subject) -> None:
        self.SUBJECT = subject
        self.MAX_TOKENS = 1000
        self.TEMPERATURE = 0.2
        self.VERBOSE = True
        self.LLM = AzureChatOpenAI(deployment_name="gpt35-team-3-0301", max_tokens=self.MAX_TOKENS, temperature=self.TEMPERATURE)
        self.MEMORY = ConversationBufferMemory(memory_key="chat_history")
        self.LLM_CHAIN = LLMChain(llm=self.LLM, prompt=get_prompt(subject))
        self.AGENT = ZeroShotAgent(llm_chain=self.LLM_CHAIN, tools=get_tools(subject), verbose=self.VERBOSE)
        self.AGENT_CHAIN = AgentExecutor.from_agent_and_tools(
            agent=self.AGENT, tools=get_tools(subject), verbose=True, memory=self.MEMORY
        )
    
    def ask(self, input_prompt):
        return self.AGENT_CHAIN.run(input_prompt)
    