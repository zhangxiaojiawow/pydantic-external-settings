# pydantic-external-settings-v1

This module provides a way to load settings from any external source, when using pydantic BaseSettings.

## Quickstart

```python
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
    bucket: ClassVar[str] = ApolloSourceConfig()

    class Config:
        env_file = '.env'


s3_settings = S3Settings()
print(s3_settings.bucket)
```

### `ExternalSourceConfig` Usage

`ExternalSourceConfig`  is a class descriptor, which can be used to load settings from any external source.
Note that the typing annotation is required to be `ClassVar` for the `ExternalSourceConfig` attribute, so that it will
not be considered as a field of the settings class. Currently, the  `ExternalSourceConfig` supports to speacify a
`validation_alias` to override the name of setting field, and a `default_value` to provide a default value when the
settings field is not found both in the external source and the inner source(like .env file and environment variables).

To use a specific external usage, like database, you can create a subclass of `ExternalSourceConfig`
and provide a callable to the `__init__` method, which will be called to get the value of the settings field. Note that
if
the field setting is not found in the external source, the callable should return None, so that the default value can be
used.