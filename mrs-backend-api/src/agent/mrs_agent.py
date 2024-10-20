from typing import List

from core.api.client.openai_client import openai_client
from core.api.packet.openai_packet import (
    ChatCompletionRequestMessage,
    CreateChatCompletionRequest,
    CreateChatCompletionResponse,
    CreateEmbeddingsRequest,
    CreateEmbeddingsResponse
)
from core.common.logger import Logger
from core.common.settings import weaviate_settings
from core.vectordb.client import weaviate_client
from packet.mrs_packet import RunMrsRequest, RunMrsResponse


class MrsAgent:
    def __init__(self):
        self._logger = Logger.get_logger(self.__class__.__name__)

    @weaviate_client.weaviate_transactional
    async def run(self, request: RunMrsRequest, client: weaviate_client.WeaviateAsyncClient = None) -> RunMrsResponse:
        utterance: str = request.question

        response: CreateEmbeddingsResponse = await openai_client.create_embeddings(
            CreateEmbeddingsRequest(
                input=utterance,
                model='text-embedding-ada-002'
            )
        )
        embedding: List[float] = response.data[0].embedding

        collection = await weaviate_client.get_collection(name=weaviate_settings.WEAVIATE_COLLECTION_NAME, client=client)
        result = await weaviate_client.near_vector(collection=collection, vector=embedding, client=client)
        context = result.objects[0].properties.get('text')
        self._logger.info(f'WEAVIATE RESULT: {context}')

        response: CreateChatCompletionResponse = await openai_client.create_chat_completion(
            CreateChatCompletionRequest(
                model='gpt-3.5-turbo',
                messages=[
                    ChatCompletionRequestMessage(
                        role='system',
                        content=context,
                    ),
                    ChatCompletionRequestMessage(
                        role='user',
                        content=utterance
                    )
                ],
                temperature=0.7
            )
        )
        self._logger.info(f'LLM RESPONSE: {response}')

        return response.choices[0].message


mrs_agent = MrsAgent()
