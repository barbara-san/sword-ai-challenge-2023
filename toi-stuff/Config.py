import os

AZURE_OPENAI_KEY = "4f8e9d40be39474c96fa1327dbd47516"
AZURE_OPENAI_ENDPOINT = "https://openai-resource-team-3-france.openai.azure.com/"
OPENAI_API_VERSION = "2023-03-15-preview"

WOLFRAM_ALPHA_APPID = "3HGHX2-433LKG3JK7"

def load_environment():
    os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_KEY
    os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_ENDPOINT
    os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["WOLFRAM_ALPHA_APPID"] = WOLFRAM_ALPHA_APPID

