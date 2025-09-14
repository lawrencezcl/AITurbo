#!/bin/bash

# AITurbo Docker 启动脚本

echo "🚀 启动 AITurbo Docker 服务..."

# 检查 docker-compose 是否存在
if ! command -v docker-compose &> /dev/null
then
    echo "❌ 未找到 docker-compose 命令，请先安装 Docker 和 Docker Compose"
    exit 1
fi

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，正在复制示例文件..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件，请编辑该文件填写配置信息后再启动服务"
    exit 0
fi

# 启动服务
echo "🐳 正在启动 Docker 服务..."
docker-compose up -d

# 检查服务状态
if [ $? -eq 0 ]; then
    echo "✅ Docker 服务启动成功！"
    echo "🌐 请访问 http://localhost:5000 使用 AITurbo"
    echo "📋 查看日志: docker-compose logs -f"
    echo "🛑 停止服务: docker-compose down"
else
    echo "❌ Docker 服务启动失败，请检查日志: docker-compose logs"
    exit 1
fi