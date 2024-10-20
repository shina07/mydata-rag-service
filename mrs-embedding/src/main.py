import asyncio
import os
from typing import Final, List

from core.common.logger import Logger
from core.common.settings import openai_settings

from embedder.document_embedder import DocumentEmbedder

logger = Logger.get_logger(__name__)


class MrsEmbedding:
    def __init__(self):
        self._documents_path: Final[str] = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'document'
        )
        self._documents: List[str] = []

        self.document_embedder: DocumentEmbedder = DocumentEmbedder()

    async def _load_document(self):
        for file in os.listdir(self._documents_path):
            filename, ext = os.path.splitext(file)

            if ext == '.pdf':
                self._documents.append(file)

        return

    async def run(self):
        logger.info(f'MyData RAG Service Document Embedder\n')

        logger.info(f'LOAD DOCUMENT START')
        await self._load_document()
        logger.info(f'LOAD DOCUMENT COMPLETE: {self._documents}')

        tasks = [
            self.document_embedder.embed(os.path.join(self._documents_path, document))
            for document in self._documents
        ]

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    mrs_embedding = MrsEmbedding()
    asyncio.run(mrs_embedding.run())
