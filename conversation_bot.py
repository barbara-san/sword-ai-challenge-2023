from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from langchain.schema import messages_from_dict, messages_to_dict
import json

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
        Current conversation:
        {chat_history}
        Human: {input}
        AI:"""

    return PromptTemplate(
        input_variables=["input", "chat_history"], template=default_template
    )

class ConversationChatBot:
    def __init__(self, subject) -> None:
        self.SUBJECT = subject
        self.MAX_TOKENS = 1000
        self.TEMPERATURE = 0.2
        self.VERBOSE = True
        self.CHAT_LMM = AzureChatOpenAI(deployment_name="gpt35-team-3-0301", max_tokens=self.MAX_TOKENS, temperature=self.TEMPERATURE)
        
        # create empty memory and save an empty json file for the memory
        self.MEMORY = ConversationBufferMemory(memory_key="chat_history", input_key="input")
        self.MEMORY_PATH = f"json_chats_memory/{self.SUBJECT}.json"
        self.save_memory() # to create the history file

        self.PROMPT = get_prompt()
        self.CONVERSATION = ConversationChain(
            llm = self.CHAT_LMM, 
            verbose = self.VERBOSE,
            memory = self.MEMORY,
            prompt = self.PROMPT
        )
        # give context
        self.ask(get_context(subject))
    
    def load_memory(self):
        with open(self.MEMORY_PATH, "r") as history:
            self.MEMORY.chat_memory.messages = messages_from_dict(json.load(history))
        history.close()

    def save_memory(self):
        with open(self.MEMORY_PATH, "w") as history:
            json.dump(messages_to_dict(self.MEMORY.chat_memory.messages), history)
        history.close()

    def ask(self, input_prompt):
        self.load_memory()
        answer = self.CONVERSATION.run(input_prompt)
        self.save_memory()
        return answer

