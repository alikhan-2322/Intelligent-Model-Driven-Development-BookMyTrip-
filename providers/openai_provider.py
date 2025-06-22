# providers/openai_provider.py

from openai_core.async_openai import AsyncOpenAI
from agents.run_context import TResponseInputItem
import json

class OpenAIProvider:
    def __init__(self, openai_client: AsyncOpenAI, use_responses: bool = False):
        self._client = openai_client
        self.use_responses = use_responses

    def get_model(self, model_name: str):
        from agents._run_impl import _OpenAIChatModel
        return _OpenAIChatModel(
            openai_client=self._client,
            model_name=model_name,
            use_responses=self.use_responses,
        )

    async def get_response(
        self,
        model: str,
        system_instructions: str,
        messages: list[TResponseInputItem],
        function_schemas: list | None = None,
        previous_response_id: str | None = None,
    ):
        # Call .create() directly – don't await it
        resp = self._client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_instructions}]
                     + [m.__dict__ if hasattr(m, "__dict__") else m for m in messages],
            temperature=0.0,
            # you can plumb through function_schemas / previous_response_id here if needed
        )

        # Convert the SDK’s ChatCompletion into what the Runner expects
        return resp
