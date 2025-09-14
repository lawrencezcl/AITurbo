#!/bin/bash

echo "🔍 检查端口冲突问题..."

# 检查常用端口是否被占用
check_port() {
    local port=$1
    local result=$(lsof -i :$port 2>/dev/null)
    if [ -n "$result" ]; then
        echo "❌ 端口 $port 被占用:"
        echo "$result"
        return 1
    else
        echo "✅ 端口 $port 可用"
        return 0
    fi
}

echo "📋 检查常用端口状态:"
echo ""

# 检查5000端口
if ! check_port 5000; then
    echo ""
    echo "🔧 5000端口被占用，已自动改为8080端口"
fi

echo ""

# 检查8080端口
if ! check_port 8080; then
    echo ""
    echo "⚠️ 8080端口也被占用，尝试其他端口..."
    
    # 寻找可用端口
    for port in 8081 8082 8083 8084 8085; do
        if check_port $port; then
            echo "🎯 找到可用端口: $port"
            echo "🔄 更新docker-compose.yml..."
            
            # 更新docker-compose.yml中的端口
            sed -i.bak "s/\"8080:5000\"/\"$port:5000\"/g" docker-compose.yml
            
            echo "✅ 已更新为端口 $port"
            AVAILABLE_PORT=$port
            break
        fi
    done
    
    if [ -z "$AVAILABLE_PORT" ]; then
        echo "❌ 没有找到可用端口，请手动检查"
        exit 1
    fi
else
    AVAILABLE_PORT=8080
fi

echo ""
echo "🚀 启动服务..."

# 停止可能存在的容器
docker-compose down --remove-orphans 2>/dev/null

# 启动服务
if docker-compose up -d; then
    echo ""
    echo "🎉 启动成功！"
    echo ""
    echo "📊 服务状态:"
    docker-compose ps
    echo ""
    echo "🌐 访问地址: http://localhost:$AVAILABLE_PORT"
    echo "📝 查看日志: docker-compose logs -f"
    echo ""
    echo "💡 提示: 如果需要改回5000端口，请先停止占用5000端口的程序"
else
    echo ""
    echo "❌ 启动失败，查看详细日志:"
    docker-compose logs
    exit 1
fi