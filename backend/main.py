"""
FastAPI 后端应用的入口。

在这里创建应用、配置跨域访问并启动开发服务器；后续还会注册业务路由。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入已读取并校验好的配置对象，通过 settings.字段名 获取配置。
from core.config import settings

# 创建 FastAPI 应用；title、description、version 是文档中展示的信息。
# docs_url 和 redoc_url 指定两种自动生成的 API 文档页面路径。
app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 添加 CORS 中间件，根据浏览器请求的来源控制跨域访问。
app.add_middleware(
    CORSMiddleware,
    # 允许的前端来源列表；协议、主机和端口都需要匹配。
    allow_origins=settings.ALLOWED_ORIGINS,
    # 允许携带凭据的跨域请求，例如 Cookie；前端也需要相应配置。
    allow_credentials=True,
    # 允许所有 HTTP 请求方法，例如 GET、POST。
    allow_methods=["*"],
    # 允许跨域请求携带任意请求头，例如 Content-Type。
    allow_headers=["*"],
)

# 直接运行此文件时才启动服务器，被其他模块导入时不执行下面的代码。
if __name__ == "__main__":
    import uvicorn

    # main:app 表示加载 main 模块中的 app 对象。
    # 0.0.0.0 表示监听所有 IPv4 网络接口，本机可通过 localhost:8000 访问。
    # reload=True 在代码变更后自动重启服务器，适用于开发阶段。
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
