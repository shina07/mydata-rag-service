from typing import Optional

from core.api.packet.base import BaseApiRequest, BaseApiResponse


class RunMrsRequest(BaseApiRequest):
    question: str


class RunMrsResponse(BaseApiResponse):
    role: str
    content: str
    refusal: Optional[bool] = None
