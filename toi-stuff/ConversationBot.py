from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory, CombinedMemory, ConversationSummaryMemory

def get_context(subject):
    return f"""\
        The following text is simply an guide that the AI must follow after receiving this text input. \
        This set of lines only exists to give context to the AI. \
        This is a friendly conversation between a human and an AI. \
        The AI serves the purpose of being a {subject} tutor. \
        The human is considered to be a highschooler learning in the Portuguese schools, which follow the portuguese teaching system. \
        The AI should help the human by giving clear detail on how to solve an exercise or how to understand a concept. \
        The AI must not use techniques that are considered to be of higher educational experience. \
        If the AI does not know the answer to a question, it truthfully says it does not know. \
        """

def get_prompt():
    default_template = """

        Summary of conversation:
        {history}
        Current conversation:
        {chat_history_lines}
        Human: {input}
        AI:"""

    return PromptTemplate(
        input_variables=["history", "input", "chat_history_lines"], template=default_template
    )

def define_memory(k_value=5):
    conv_memory = ConversationBufferWindowMemory(
        memory_key="chat_history_lines",
        input_key="input",
        k=k_value
    )
    summary_memory = ConversationSummaryMemory(llm=AzureChatOpenAI(deployment_name="gpt35-team-3-0301"), input_key="input")
    return CombinedMemory(memories=[conv_memory, summary_memory])

class ConversationChatBot:
    def __init__(self, subject) -> None:
        self.SUBJECT = subject
        self.MAX_TOKENS = 1000
        self.TEMPERATURE = 0.2
        self.VERBOSE = True
        self.CHAT_LMM = AzureChatOpenAI(deployment_name="gpt35-team-3-0301", max_tokens=self.MAX_TOKENS, temperature=self.TEMPERATURE)
        self.MEMORY = define_memory(k_value=2)
        self.PROMPT = get_prompt()
        self.CONVERSATION = ConversationChain(
            llm = self.CHAT_LMM, 
            verbose = self.VERBOSE,
            memory = self.MEMORY,
            prompt = self.PROMPT
        )
        # give context
        self.ask(get_context(subject))

    def ask(self, input_prompt):
        return self.CONVERSATION.run(input_prompt)

