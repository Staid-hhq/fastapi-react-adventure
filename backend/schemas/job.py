"""
故事生成任务的 API 数据格式模块。

定义创建任务和查询任务时的数据格式，校验 API 请求并组织响应。
"""

from typing import  Optional
from datetime import datetime
from pydantic import BaseModel


class StoryJobBase(BaseModel):
    # 创建故事生成任务所需的主题，必须提供字符串。
    theme: str


class StoryJobResponse(BaseModel):
    # 对外使用的任务标识，与数据库模型的字符串 job_id 对应。
    job_id: str
    # 当前状态由业务代码提供；此处仅校验它是字符串。
    status: str
    # 任务创建时间；响应转成 JSON 时会序列化为日期时间字符串。
    created_at: datetime
    # 以下字段允许省略或为 None，适用于任务尚未完成或没有错误的情况。
    story_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        # 允许直接读取 StoryJob 等 ORM 对象的同名属性来构造响应。
        from_attributes = True


class StoryJobCreate(StoryJobBase):
    # 继承 theme，暂不增加字段；独立命名便于以后扩展创建任务的请求格式。
    pass
