from pydantic_external_settings import ExternalSourceConfig
from pydantic import BaseSettings
from typing import ClassVar


class ApolloSourceConfig(ExternalSourceConfig):
    def __init__(self, validation_alias: str = None, *, default_value=None):
        super().__init__(self.get_from_apollo, validation_alias, default_value=default_value)

    def get_from_apollo(self, key):
        return key + "_***"


class S3Settings(BaseSettings):
    api_key: str = "api_key"
    bucket: ClassVar[str] = ApolloSourceConfig(default_value='bucket_default')

    class Config:
        env_file = '.env'


s3_settings = S3Settings()
print(s3_settings.bucket)
