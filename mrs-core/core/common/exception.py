from typing import Optional


class MrsServiceException(Exception):
    def __init__(self, code: int, message: Optional[str] = None):
        self.code = code
        self.message = message or 'MRS Service Exception'

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(code={self.code}, message={self.message}'
