#!/bin/bash

echo "🛠️ 修复Docker内存问题..."

# 检查Docker Desktop内存配置
echo "📊 检查Docker Desktop内存配置:"
echo "请确保Docker Desktop分配了至少4GB内存"
echo ""
echo "📋 配置步骤:"
echo "1. 打开Docker Desktop"
echo "2. 点击设置 ⚙️"
echo "3. 选择 'Resources' -> 'Advanced'"
echo "4. 将内存调整到至少4GB"
echo "5. 点击 'Apply & Restart'"
echo ""

read -p "是否已经调整了Docker内存配置？(y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "请先调整Docker内存配置再继续"
    exit 1
fi

# 清理Docker缓存
echo "🧹 清理Docker缓存..."
docker system prune -f
docker builder prune -f

# 检查是否使用轻量级Dockerfile
echo "🤔 选择构建方式:"
echo "1. 使用标准Dockerfile（需要更多内存）"
echo "2. 使用轻量级Dockerfile（推荐，Alpine Linux）"
echo ""
read -p "请选择 (1/2): " -n 1 -r
echo

if [[ $REPLY =~ ^[2]$ ]]; then
    echo "✅ 使用轻量级构建..."
    # 备份原Dockerfile
    cp Dockerfile Dockerfile.backup
    # 使用轻量级版本
    cp Dockerfile.lightweight Dockerfile
    echo "已切换到轻量级Dockerfile"
fi

# 停止现有服务
echo "⏹️ 停止现有服务..."
docker-compose down --remove-orphans

# 设置Docker构建参数（限制内存使用）
export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain

echo "🚀 开始构建（使用内存优化参数）..."
echo "⏳ 这可能需要一些时间，请耐心等待..."

# 使用内存限制构建
if docker-compose build --memory=2g app; then
    echo "✅ 构建成功！"
    
    # 启动服务
    echo "🚀 启动服务..."
    if docker-compose up -d; then
        echo ""
        echo "🎉 部署成功！"
        echo ""
        echo "📊 服务状态:"
        docker-compose ps
        echo ""
        echo "🌐 访问地址: http://localhost:8080"
        echo "📝 查看日志: docker-compose logs -f"
    else
        echo "❌ 启动失败，查看日志: docker-compose logs"
        exit 1
    fi
else
    echo "❌ 构建失败"
    echo ""
    echo "🔧 其他解决方案:"
    echo "1. 增加Docker Desktop内存分配（推荐8GB）"
    echo "2. 重启电脑释放内存"
    echo "3. 关闭其他占用内存的应用"
    echo "4. 使用云服务器部署"
    
    # 恢复原Dockerfile（如果备份了）
    if [[ -f Dockerfile.backup ]]; then
        mv Dockerfile.backup Dockerfile
        echo "已恢复原Dockerfile"
    fi
    
    exit 1
fi