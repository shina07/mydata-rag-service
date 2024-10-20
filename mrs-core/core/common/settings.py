import os

from pydantic_settings import BaseSettings, SettingsConfigDict


PROFILE = os.getenv('PROFILE', 'local')
CORE_ENV_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    f'env/.env.{PROFILE}'
)

config_dict: SettingsConfigDict = SettingsConfigDict(
    extra='ignore',
    env_file=CORE_ENV_FILE
)


class CoreSettings(BaseSettings):
    model_config: SettingsConfigDict = config_dict

    ENVIRONMENT: str


class OpenAISettings(BaseSettings):
    model_config: SettingsConfigDict = config_dict

    OPENAI_API_KEY: str

    OPENAI_CHAT_COMPLETION_ENDPOINT: str
    OPENAI_EMBEDDINGS_ENDPOINT: str


class WeaviateSettings(BaseSettings):
    model_config: SettingsConfigDict = config_dict

    WEAVIATE_HTTP_HOST: str
    WEAVIATE_HTTP_PORT: int
    WEAVIATE_HTTP_SECURE: bool
    WEAVIATE_GRPC_HOST: str
    WEAVIATE_GRPC_PORT: int
    WEAVIATE_GRPC_SECURE: bool

    WEAVIATE_COLLECTION_NAME: str


core_settings = CoreSettings()
openai_settings = OpenAISettings()
weaviate_settings = WeaviateSettings()
