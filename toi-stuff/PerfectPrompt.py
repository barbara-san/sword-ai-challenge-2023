import os
from langchain.chat_models import AzureChatOpenAI

AZURE_OPENAI_KEY = "4f8e9d40be39474c96fa1327dbd47516"
AZURE_OPENAI_ENDPOINT = "https://openai-resource-team-3-france.openai.azure.com/"
OPENAI_API_VERSION = "2023-03-15-preview"

os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_KEY
os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_ENDPOINT
os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
os.environ["OPENAI_API_TYPE"] = "azure"

better_prompt_llm = AzureChatOpenAI(deployment_name="gpt35-team-3-0301", temperature= 0.2)

def better_prompt(prompt):
    return better_prompt_llm.predict(
        f"""\
        The AI must process the prompt and alter it in order to make it more accurate and understandable for any LLM model. \
        The context and idea of the given prompt MUST remain inaltered. \
        The new prompt may include new additional text that is predictable to be presented by the human in the future. \
        You must always not interpret the prompts as a question or information for yourself. \
        Your ONLY job is to process the given prompt by the steps described above. \
        \
        Prompt: \
        ```\
        {prompt}\
        ```\
        \
        You MUST only return the new prompt, and nothing else.\
        """
    )