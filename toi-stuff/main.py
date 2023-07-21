from agent_bot import AgentChatBot
from conversation_bot import ConversationChatBot
from perfect_bot import perfect_prompt
from decision_bot import need_agent

from config import load_environment

from subjects_and_tools import *


subject = MATHS


agent = AgentChatBot(subject)
conversation = ConversationChatBot(subject)


def ask_chat(input_prompt):
    if input_prompt == "X":
        return "AAAA"
    #new_input_prompt = perfect_prompt(input_prompt)
    #print(f"\n\"Better\" input:\n\t{new_input_prompt}\n")
    answer = agent.ask(input_prompt) if need_agent(input_prompt) else conversation.ask(input_prompt)
    return answer


if __name__ == "__main__":
    load_environment()
    while True:
        prompt = input("Input:\n\t")
        if prompt == "X":
            break
        answer = ask_chat(prompt)
        print(f"Output:\n\t{answer}")


        