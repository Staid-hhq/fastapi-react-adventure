"""
数据库连接与会话管理模块。

配置 SQLAlchemy 引擎、会话工厂和模型基类，提供会话获取与建表函数。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

# 引擎根据连接地址管理数据库连接；创建引擎时通常还不会真正连接数据库。
engine = create_engine(
    settings.DATABASE_URL
)

# 会话工厂：每次调用 SessionLocal() 都会创建一个独立的 Session。
# autocommit=False：修改需要显式 commit() 才会提交。
# autoflush=False：查询前不自动同步待写入的数据，但 commit() 仍会触发 flush。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 所有数据库模型继承同一个 Base，表结构会登记到 Base.metadata 中。
Base = declarative_base()


def get_db():
    # 后续在 FastAPI 路由中通过 Depends(get_db) 获取本次请求使用的会话。
    db = SessionLocal()
    try:
        # 将会话交给路由使用；提交事务由调用方负责。
        yield db
    finally:
        # 依赖清理时执行，即使发生异常也关闭会话，释放其占用的连接资源。
        db.close()


def create_tables():
    # 调用前先导入模型模块，确保需要的表已登记到 Base.metadata。
    # 只创建尚不存在的表；不会自动修改已有表的字段或执行数据库迁移。
    Base.metadata.create_all(bind=engine)
