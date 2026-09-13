"""
冒险故事的 API 数据格式模块。

定义故事接口的请求与响应格式，由 Pydantic 负责数据校验和序列化。
这里描述 API 传输的数据；models 中的 SQLAlchemy 模型描述数据库表。
"""

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel


class StoryOptionsSchema(BaseModel):
    # 展示给用户的选项文字，以及选择后跳转到的节点 ID。
    text: str
    # Optional 允许 None，= None 表示省略字段时也使用 None。
    node_id: Optional[int] = None


class StoryNodeBase(BaseModel):
    # 节点共有字段：正文必填，两个结局标记省略时默认为 False。
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False


class CompleteStoryNodeResponse(StoryNodeBase):
    # 继承正文和结局标记，再补充返回给前端的节点 ID 与选项列表。
    id: int
    # 每个选项按 StoryOptionsSchema 校验；Pydantic 会为实例复制此空列表默认值。
    options: List[StoryOptionsSchema] = []

    class Config:
        # 允许 model_validate() 从 ORM 对象的同名属性读取数据，而不只接受字典。
        from_attributes = True


class StoryBase(BaseModel):
    # 故事共有字段：标题必填，业务会话标识可省略或为 None。
    title: str
    session_id: Optional[str] = None

    class Config:
        from_attributes = True


class CreateStoryRequest(BaseModel):
    # 创建故事时客户端提交的请求体，例如 {"theme": "森林冒险"}。
    theme: str


class CompleteStoryResponse(StoryBase):
    # 继承标题和会话标识；返回完整故事时还必须提供以下字段。
    id: int
    # Python 中使用 datetime，序列化为 JSON 时转换为日期时间字符串。
    created_at: datetime
    # 故事的起始节点，需要业务代码从故事节点中选出。
    root_node: CompleteStoryNodeResponse
    # 按节点 ID 查找完整节点数据；JSON 对象的键在序列化后会变成字符串。
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:
        # 只读取同名属性，不会自动把 Story.nodes 转成 root_node 和 all_nodes。
        # 这两个字段需要在构造完整响应时由业务代码组装。
        from_attributes = True
