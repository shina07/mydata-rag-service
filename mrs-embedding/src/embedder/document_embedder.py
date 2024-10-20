import asyncio
from typing import List

from core.common.logger import Logger
from pypdf import PdfReader, PageObject
from core.common.settings import weaviate_settings
from concurrent.futures import ThreadPoolExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.api.client.openai_client import openai_client
from core.api.packet.openai_packet import CreateEmbeddingsRequest, CreateEmbeddingsResponse
from core.vectordb.client import weaviate_client
logger = Logger.get_logger(__name__)


class DocumentEmbedder:
    def __init__(self):
        self._text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=50)

    async def embed(self, file_path: str) -> None:
        chunks = await self.extract_text_chunk(path=file_path)
        # logger.info(f'text: {chunks[0]}')

        embeddings = await self.generate_embeddings(chunks=chunks)
        logger.info(f'embeddings: {embeddings}')

        await self.insert_vectors(chunks=chunks, embeddings=embeddings)


    async def extract_text_chunk(self, path: str):
        pdf_reader = PdfReader(path)
        logger.info(f'EXTRACT PAGE: {path}')
        logger.info(f'TOTAL PAGES: {len(pdf_reader.pages)}')

        with ThreadPoolExecutor() as executor:
            chunks: List[List[str]] = list(executor.map(self._extract_text_chunk_from_page, pdf_reader.pages))

        print(f'CHUNK LEN: {len(chunks)}')

        return [chunk for page_chunks in chunks for chunk in page_chunks]

    def _extract_text_chunk_from_page(self, page: PageObject) -> List[str]:
        """
        MultiThreading 실행을 위한 synchronous Function

        :param page: PyPDF2.PageObject page
        :return: List[str] text chunks from page
        """
        text = page.extract_text()
        return self._text_splitter.split_text(text)

    async def generate_embeddings(self, chunks: List[str]) -> List[CreateEmbeddingsResponse]:
        tasks = [
            openai_client.create_embeddings(
                CreateEmbeddingsRequest(
                    input=chunk,
                    model='text-embedding-ada-002'
                )
            )
            for chunk in chunks
        ]

        embeddings = await asyncio.gather(*tasks)
        logger.info(f'Generated embeddings: {len(embeddings)}')

        return [embedding.data[0].embedding for embedding in embeddings]

    @weaviate_client.weaviate_transactional
    async def insert_vectors(
            self,
            chunks: List[str],
            embeddings: List[List[float]],
            client: weaviate_client.WeaviateAsyncClient = None
    ):
        collection = await weaviate_client.get_collection(name=weaviate_settings.WEAVIATE_COLLECTION_NAME, client=client)
        logger.info(f'WEAVIATE COLLECTION: {collection}')

        for chunk, embedding in zip(chunks, embeddings):
            await weaviate_client.insert(collection=collection, vector=embedding, properties={"text": chunk}, client=client)

        await self.test(collection=collection, client=client)

    @weaviate_client.weaviate_transactional
    async def test(self, collection, client: weaviate_client.WeaviateAsyncClient = None):
        async for item in collection.iterator(include_vector=True):
            logger.info(f'ITEM: {item}')
