# 使用官方 Python 精简版镜像
FROM python:3.11-slim

# 安装系统依赖和 mkcert
RUN apt update && apt install -y \
    libnss3-tools curl ca-certificates openssl && \
    curl -L -o /usr/local/bin/mkcert https://github.com/FiloSottile/mkcert/releases/latest/download/mkcert-v1.4.4-linux-amd64 && \
    chmod +x /usr/local/bin/mkcert

# 初始化根证书（第一次运行容器时执行）
RUN mkcert -install

# 设置工作目录
WORKDIR /app

# 复制项目代码
COPY . .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建证书目录（用于存储 mkcert 生成的证书）
RUN mkdir -p certs

# 暴露服务端口
EXPOSE 8000

# 启动 FastAPI 服务
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
