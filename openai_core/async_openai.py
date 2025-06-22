from openai import OpenAI

class AsyncOpenAI(OpenAI):
    """
    No-op subclass of OpenAI client that we import as 'async'.
    """
    pass
