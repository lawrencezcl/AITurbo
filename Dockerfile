# 轻量级Dockerfile - 针对低内存环境优化
FROM python:3.11-alpine

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖（Alpine包更小）
RUN apk add --no-cache \
        gcc \
        musl-dev \
        mariadb-connector-c-dev \
        pkgconfig \
        && rm -rf /var/cache/apk/*

# 复制requirements.txt文件
COPY requirements.txt .

# 安装Python依赖（使用国内镜像源）
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
        Flask>=3.1.1 \
        Werkzeug>=3.1.3 \
        gunicorn>=23.0.0 \
        requests>=2.32.4 \
        beautifulsoup4>=4.12.0 \
        PyMySQL>=1.1.0 \
        APScheduler>=3.7.0 \
        email-validator>=2.2.0 \
        typing-extensions>=4.0.0

# 单独安装可能有问题的包
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
        google-genai>=1.25.0 || \
    pip install --no-cache-dir google-genai>=1.25.0

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
        dashscope>=1.14.0 || \
    pip install --no-cache-dir dashscope>=1.14.0

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
        openai>=1.0.0 || \
    pip install --no-cache-dir openai>=1.0.0

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p cache data logs config

# 设置启动脚本权限
RUN chmod +x start_app.sh

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["./start_app.sh"]