import aiohttp

from core.common.logger import Logger
from core.api.packet.base import BaseApiRequest, BaseApiResponse

logger = Logger.get_logger(__name__)


class BaseApiClient:
    def __init__(self, tag: str):
        self.api = tag

    async def post(self, url: str, request: BaseApiRequest = None) -> dict:

        data: dict = request.model_dump()

        async with aiohttp.ClientSession() as session:
            logger.debug(f'[{self.api}] POST REQUEST: {url} :: DATA: {data}')

            async with session.post(url, json=data) as response:
                return await response.json()
