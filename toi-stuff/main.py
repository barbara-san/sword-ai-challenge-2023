from PerfectPrompt import better_prompt
from AgentBot import AgentChatBot
from ConversationBot import ConversationChatBot

from Config import load_environment
load_environment()

from DecisionBot import need_agent


MATHS = "Mathematics"
HISTORY = "History"


if __name__ == "__main__":

    subject = HISTORY

    agent = AgentChatBot(subject)
    conversation = ConversationChatBot(subject)

    while True:
        input_prompt = input("\nOriginal input:\n\t")
        if input_prompt == "X":
            break
        new_input_prompt = better_prompt(input_prompt)
        print(f"\n\"Better\" input:\n\t{new_input_prompt}")
        answer = agent.ask(new_input_prompt) if need_agent(new_input_prompt) else conversation.ask(new_input_prompt)
        print(f"Output:\n\t{answer}\n")
