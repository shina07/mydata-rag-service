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


class OpenaiSettings(BaseSettings):
    model_config: SettingsConfigDict = config_dict

    OPENAI_API_KEY: str


core_settings = CoreSettings()
openai_settings = OpenaiSettings()
