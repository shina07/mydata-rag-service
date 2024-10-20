from functools import wraps
from typing import Optional, List
from uuid import UUID

from weaviate import WeaviateAsyncClient
from weaviate.collections import CollectionAsync
from weaviate.connect import ConnectionParams

from core.common.logger import Logger
from core.common.settings import weaviate_settings

logger = Logger.get_logger(__name__)


connection_params = ConnectionParams.from_params(
    http_host=weaviate_settings.WEAVIATE_HTTP_HOST,
    http_port=weaviate_settings.WEAVIATE_HTTP_PORT,
    http_secure=weaviate_settings.WEAVIATE_HTTP_SECURE,
    grpc_host=weaviate_settings.WEAVIATE_GRPC_HOST,
    grpc_port=weaviate_settings.WEAVIATE_GRPC_PORT,
    grpc_secure=weaviate_settings.WEAVIATE_GRPC_SECURE,
)


class AsyncClientContext:
    def __init__(self):
        self.client: Optional[WeaviateAsyncClient] = None

    async def __aenter__(self):
        self.client = WeaviateAsyncClient(connection_params=connection_params)
        await self.client.connect()
        logger.info(f'[AENTER] Connected to weaviate: {self.client}')

        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()
        logger.info(f'[AEXIT] weaviate closed: {self.client}')

        self.client = None


def weaviate_transactional(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):

        # Client Session Provided
        if 'weaviate_client' in kwargs:
            return await func(*args, **kwargs)

        else:
            async with AsyncClientContext() as client:
                kwargs['weaviate_client'] = client

                try:
                    return await func(*args, **kwargs)

                except Exception as e:
                    raise e

    return wrapper


@weaviate_transactional
async def is_ready(weaviate_client: WeaviateAsyncClient = None) -> bool:
    return await weaviate_client.is_ready()


@weaviate_transactional
async def create_collection(name: str, weaviate_client: WeaviateAsyncClient = None) -> CollectionAsync:
    return await weaviate_client.collections.create(name=name)


@weaviate_transactional
async def list_collection(weaviate_client: WeaviateAsyncClient = None):
    return await weaviate_client.collections.list_all()


@weaviate_transactional
async def get_collection(name: str, weaviate_client: WeaviateAsyncClient = None) -> CollectionAsync:
    return await weaviate_client.collections.get(name=name)


@weaviate_transactional
async def insert(collection: CollectionAsync, vector: List[float], properties: dict, weaviate_client: WeaviateAsyncClient = None) -> UUID:
    return await collection.data.insert(vector=vector, properties=properties)


@weaviate_transactional
async def insert_data_many(collection: CollectionAsync, data: List[dict], weaviate_client: WeaviateAsyncClient = None) -> UUID:
    return await collection.data.insert_many(objects=data)


@weaviate_transactional
async def near_vector(collection: CollectionAsync, vector: List[float], weaviate_client: WeaviateAsyncClient = None) -> UUID:
    return await collection.query.near_vector(near_vector=vector, limit=2)
