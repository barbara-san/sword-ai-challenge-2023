from promptbot import better_prompt
from agentbot import AgentChatBot
from conversationbot import ConversationChatBot

from config import load_environment
load_environment()

from decisionbot import need_agent


MATH = "mathematics"
HISTORY = "history"


subject = HISTORY
chats = {
    "mathematics" : "",
    "history" : ""
}

agent = AgentChatBot(subject)
conversation = ConversationChatBot(subject)

def ask_chat(input_prompt):
    if input_prompt == "X":
        return "AAAA "
    new_input_prompt = better_prompt(input_prompt)
    answer = agent.ask(new_input_prompt) if need_agent(new_input_prompt) else conversation.ask(new_input_prompt)
    return answer

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    #return ask_chat("Hi! I need help with my homework, can you help me?")

@app.route('/<id>', methods=['GET', 'POST'])
def subject(id):
    if request.method == 'POST':
        expr = request.form.get('data')
        chats[id] += "<strong>You: </strong>" + expr + "<p></p>";
        chats[id] += id + " tutor: " + ask_chat(expr) + "<p></p>"
    return render_template('subject.html',
                            subject=id, conversation=chats[id])



if __name__ == "__main__":
    app.run()