import os

from core.api.client.base import BaseApiClient
from core.api.packet.openai_packet import (
    CreateChatCompletionRequest,
    CreateChatCompletionResponse,
    CreateEmbeddingsRequest,
    CreateEmbeddingsResponse
)
from core.common.settings import openai_settings


class OpenAIClient(BaseApiClient):
    def __init__(self):
        super(OpenAIClient, self).__init__(tag='OpenAI', api_key=openai_settings.OPENAI_API_KEY)

    async def create_chat_completion(self, request: CreateChatCompletionRequest) -> CreateChatCompletionResponse:
        response = await self.post(url=openai_settings.OPENAI_CHAT_COMPLETION_ENDPOINT, request=request)
        return CreateChatCompletionResponse.model_validate(response)

    async def create_embeddings(self, request: CreateEmbeddingsRequest) -> CreateEmbeddingsResponse:
        response = await self.post(url=openai_settings.OPENAI_EMBEDDINGS_ENDPOINT, request=request)
        print(response)
        return CreateEmbeddingsResponse.model_validate(response)


openai_client = OpenAIClient()
