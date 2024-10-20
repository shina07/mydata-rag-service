import aiohttp

from core.common.logger import Logger
from core.api.packet.base import BaseApiRequest, BaseApiResponse

logger = Logger.get_logger(__name__)


class BaseApiClient:
    def __init__(self, tag: str, api_key: str = None):
        self.api = tag
        self._default_headers = {
            'Authorization': f'Bearer {api_key}' if api_key else None,
            'Content-Type': 'application/json'
        }

    async def post(self, url: str, request: BaseApiRequest = None) -> dict:

        data: dict = request.model_dump()

        async with aiohttp.ClientSession() as session:
            logger.debug(f'[{self.api}] POST REQUEST: {url} :: DATA: {data}')

            async with session.post(url, headers=self._default_headers, json=data) as response:
                return await response.json()
