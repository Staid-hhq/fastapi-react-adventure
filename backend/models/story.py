"""
冒险故事的数据库模型模块。

定义故事和故事节点如何存入数据库：一个故事对应多个节点。
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class Story(Base):
    # 数据库中的实际表名；一个 Story 对象对应表中的一条记录。
    __tablename__ = "stories"

    # 主键唯一标识故事；index=True 声明索引，供数据库查找使用。
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    # 业务会话标识，用于区分故事所属的会话，与 SQLAlchemy Session 不同。
    session_id = Column(String, index=True)
    # 插入记录时由数据库生成创建时间；时区支持取决于所用数据库。
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 一对多关系：story.nodes 访问此故事的节点列表。
    # back_populates 指向 StoryNode.story，与另一端的关系属性配对。
    nodes = relationship("StoryNode", back_populates="story")


class StoryNode(Base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    # 外键记录所属故事的主键；它连接的是 stories 表的 id 列。
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    # 当前节点展示的故事正文。
    content = Column(String)
    # 分别标记：是否为起点、是否为结局、是否为胜利结局。
    # default 在插入时未提供该字段值的情况下生效。
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)
    # 选项以 JSON 保存，例如 [{"text": "进入森林", "node_id": 2}]。
    # default=list 在插入时为缺省值生成新的空列表；JSON 列本身不校验选项结构。
    options = Column(JSON, default=list)

    # 多对一关系：node.story 访问所属故事；relationship 本身不是数据库列。
    story = relationship("Story", back_populates="nodes")
