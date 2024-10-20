from typing import List, Union, Optional

from pydantic import BaseModel

from core.api.packet.base import BaseApiRequest, BaseApiResponse
from core.common.constant import StrEnum, auto


# Chat Completion
class ChatCompletionRequestMessage(BaseModel):
    role: str
    content: str


class ChatCompletionResponseMessage(BaseModel):
    role: str
    content: str
    refusal: Optional[bool] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatCompletionResponseMessage
    # logprobs:
    finish_reason: str


class ChatCompletionResponseUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    # prompt_tokens_details
    # completion_tokens_details


class CreateChatCompletionRequest(BaseApiRequest):
    model: str
    messages: List[ChatCompletionRequestMessage]
    temperature: Optional[float] = None


class CreateChatCompletionResponse(BaseApiResponse):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: ChatCompletionResponseUsage
    system_fingerprint: Optional[str] = None


# Embedding
class EmbeddingsEncodingFormat(StrEnum):
    float = auto()
    base64 = auto()


class EmbeddingResponseObject(BaseModel):
    object: str
    embedding: List[float]
    index: int


class EmbeddingResponseUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class CreateEmbeddingsRequest(BaseApiRequest):
    input: Union[str, List[str]]
    model: str
    # encoding_format: Optional[EmbeddingsEncodingFormat]
    # dimensions: Optional[int]
    # user: Optional[str]


class CreateEmbeddingsResponse(BaseApiResponse):
    object: str
    data: List[EmbeddingResponseObject]
    model: str
    # usage: EmbeddingResponseUsage
