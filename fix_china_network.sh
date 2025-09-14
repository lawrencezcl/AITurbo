#!/bin/bash

echo "🇨🇳 配置中国大陆网络优化..."

# 检查Docker是否运行
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker Desktop"
    exit 1
fi

echo "✅ Docker正在运行"

# 检查并提示配置镜像加速
echo "📝 检查Docker镜像加速配置..."
mirrors=$(docker info 2>/dev/null | grep -A 10 "Registry Mirrors" | grep -c "http")
if [ "$mirrors" -eq 0 ]; then
    echo "⚠️  未检测到镜像加速配置！"
    echo "🔧 请手动配置 Docker Desktop:"
    echo "   1. 打开 Docker Desktop"
    echo "   2. 点击右上角设置图标 ⚙️"
    echo "   3. 选择 'Docker Engine'"
    echo "   4. 替换配置为 daemon.json文件的内容"
    echo "   5. 点击 'Apply & Restart'"
    echo ""
    read -p "是否已经配置完成？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "请先配置镜像加速再运行此脚本"
        exit 1
    fi
else
    echo "✅ 已配置 $mirrors 个镜像加速地址"
fi

# 清理之前的容器和镜像
echo "🧹 清理旧的容器和镜像..."
docker-compose down --remove-orphans 2>/dev/null
docker system prune -f

# 显示当前Docker镜像源配置
echo "📋 当前Docker配置:"
docker info | grep -A 5 "Registry Mirrors" || echo "未配置镜像源"

echo ""
echo "🚀 开始构建项目..."
echo "⏳ 首次构建可能需要5-10分钟，请耐心等待..."
echo "📝 如果仍然失败，请尝试使用科学上网工具"

# 构建并启动
if docker-compose up -d --build; then
    echo ""
    echo "🎉 构建成功！"
    echo ""
    echo "📊 服务状态:"
    docker-compose ps
    echo ""
    echo "🌐 访问地址: http://localhost:8080"
    echo "📝 查看日志: docker-compose logs -f"
    echo ""
    echo "💡 如果有问题，请查看 CHINA_DEPLOYMENT_GUIDE.md"
else
    echo ""
    echo "❌ 构建失败，请检查网络连接"
    echo ""
    echo "🔧 建议解决方案:"
    echo "1. 确保已配置 Docker 镜像加速（参考 daemon.json 文件）"
    echo "2. 检查网络连接"
    echo "3. 尝试使用科学上网工具"
    echo "4. 手动拉取镜像: docker pull mysql:8.0"
    echo "5. 查看详细日志: docker-compose logs"
    exit 1
fi