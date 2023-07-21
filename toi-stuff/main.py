from AgentBot import AgentChatBot
from ConversationBot import ConversationChatBot
from PerfectPrompt import perfect_prompt

from Config import load_environment

from DecisionBot import need_agent


MATHS = "Mathematics"
HISTORY = "History"


subject = HISTORY


agent = AgentChatBot(subject)
conversation = ConversationChatBot(subject)


def ask_chat(input_prompt):
    if input_prompt == "X":
        return "AAAA"
    new_input_prompt = perfect_prompt(input_prompt, conversation.MEMORY)
    print(f"\n\"Better\" input:\n\t{new_input_prompt}\n")
    answer = agent.ask(new_input_prompt) if need_agent(new_input_prompt) else conversation.ask(new_input_prompt)
    return answer


if __name__ == "__main__":
    load_environment()
    while True:
        prompt = input("Input:\n\t")
        if prompt == "X":
            break
        answer = ask_chat(prompt)
        print(f"Output:\n\t{answer}")

    #print(conversation.MEMORY.memories[-1].)

        