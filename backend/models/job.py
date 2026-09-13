"""
故事生成任务的数据库模型模块。

保存故事生成任务的标识、状态、结果和时间，供后续查询任务进度。
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.database import Base


class StoryJob(Base):
    __tablename__ = "story_jobs"

    # 数据库内部的整数主键。
    id = Column(Integer, primary_key=True, index=True)
    # 对外查询任务使用的字符串标识，例如 UUID；unique=True 禁止重复。
    # 这里仅定义存储字段，具体标识需要由业务代码生成。
    job_id = Column(String, index=True, unique=True)
    # 任务所属的业务会话，以及用户提供的故事主题。
    session_id = Column(String, index=True)
    theme = Column(String)
    # 由业务代码更新的状态字符串；当前模型没有限制允许的状态值。
    status = Column(String)
    # 生成成功后的故事 ID；nullable=True 允许任务未完成时保存 NULL。
    # 当前是普通整数列，没有声明 ForeignKey，不会在数据库层约束故事是否存在。
    story_id = Column(Integer, nullable=True)
    # 失败时记录错误信息；没有错误时可为空。
    error = Column(String, nullable=True)
    # 创建时间由数据库生成，完成时间需要在任务结束时由业务代码写入。
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
