"""
项目配置模块。

统一读取并校验配置，供应用、数据库连接和故事生成等功能使用。
具体配置项随视频实现；密钥等本地配置放在 .env 中。
"""

from typing import Annotated, List
from pydantic_settings import BaseSettings, NoDecode
from pydantic import field_validator


# BaseSettings 读取配置并转换为声明的类型。
# 未显式传参时，系统环境变量通常优先于 .env，未提供的值使用字段默认值。
class Settings(BaseSettings):
    # 业务 API 的公共路径前缀，后续注册路由时需要显式使用才会生效。
    API_PREFIX: str = "/api"
    # 将 .env 中的 True 等文本转成布尔值，不会自动控制服务器的 debug 或 reload。
    DEBUG: bool = False

    # 数据库连接地址；这里只保存字符串，后续由数据库模块建立连接。
    DATABASE_URL: str = ""

    # 没有默认值，必须提供此配置项；当前允许空字符串占位。
    # 后续调用 OpenAI 时需要有效密钥，不要在日志中打印它。
    OPENAI_API_KEY: str

    # 最终值是字符串列表。Annotated 附加 NoDecode，关闭默认的 JSON 解码，
    # 让下面的校验器处理用逗号分隔的地址文本。
    ALLOWED_ORIGINS: Annotated[List[str], NoDecode] = []

    # before：先转换原始输入，再检查是否符合列表类型。
    @field_validator("ALLOWED_ORIGINS", mode="before")
    # 类方法中的 cls 代表 Settings 类，而不是某个配置实例。
    @classmethod
    def parse_allowed_origins(cls, v):
        # 输入是逗号分隔的地址字符串时，将其拆成列表；空字符串转为空列表。
        if isinstance(v, str):
            return v.split(",") if v else []
        # 输入已经是列表时直接返回，交给 Pydantic 继续校验。
        return v

    # 配置文件的读取规则。
    class Config:
        # 相对于运行时工作目录查找；当前应从 backend 目录启动程序。
        env_file = ".env"
        # 使用 UTF-8 读取文件，支持中文注释。
        env_file_encoding = "utf-8"
        # 配置名按大小写匹配，.env 中沿用全大写字段名。
        # Windows 系统环境变量本身不区分大小写，不受此选项约束。
        case_sensitive = True


# 导入本模块时创建配置实例，触发配置读取、类型转换和校验。
settings = Settings()
