"""
项目配置模块。

后续统一读取环境变量等配置，供数据库连接和故事生成等功能使用。
具体配置项随视频实现；密钥等本地配置放在 .env 中。
"""

from typing import Annotated, List
from pydantic_settings import BaseSettings, NoDecode
from pydantic import field_validator


class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False

    DATABASE_URL: str = ""

    OPENAI_API_KEY: str

    ALLOWED_ORIGINS: Annotated[List[str], NoDecode] = []

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            return v.split(",") if v else []
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
