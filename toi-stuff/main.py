from PerfectPrompt import better_prompt
from AgentBot import AgentChatBot
from ConversationBot import ConversationChatBot

from Environment import load_environment
load_environment()

SUBJECT = "History"

agent = AgentChatBot(SUBJECT)
conversation = ConversationChatBot(SUBJECT)

while True:
    input_prompt = input("\nOriginal input:\n\t")
    if input_prompt == "X":
        break
    new_input_prompt = better_prompt(input_prompt)
    print(f"\n\"Better\" input:\n\t{new_input_prompt}")
    answer = agent.ask(new_input_prompt)
    print(f"Output:\n\t{answer}\n")
