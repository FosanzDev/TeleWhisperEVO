from openai import AsyncOpenAI

class GenAIConnector:

    def __init__(self, api_key):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)