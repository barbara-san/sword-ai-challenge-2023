# subjects
MATHS = "Mathematics"
HISTORY = "History"
PORTUGUESE = "Portuguese"
ENGLISH = "English (Secondary Language)"
PHY_CHEM = "Physics and Chemistry"
BIO_GEO = "Biology and Geology"
PHILOSOPHY = "Philosophy"

# import packages
from langchain.agents import Tool
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper

# load env. variables
from config import load_environment
load_environment()

# APIs
wolframalpha_api = WolframAlphaAPIWrapper()
wikipedia_api = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# tools
wolframalpha = Tool(
    name="Math Helper (WolframAlpha)",
    func=wolframalpha_api.run,
    description="useful for when you need to answer questions math related"
)
wikipedia = Tool(
    name="Wikipedia Helper",
    func=wikipedia_api.run,
    description="useful for when you need to search about any topic and get some historical knowledge from it"
)

# tools mapping
TOOLS_OF = {
    MATHS : [wolframalpha],
    HISTORY : [wikipedia],
    PORTUGUESE : [wikipedia],
    ENGLISH : [wikipedia],
    PHY_CHEM : [wolframalpha, wikipedia],
    BIO : [wolframalpha, wikipedia],
    PHILOSOPHY : [wikipedia]
}