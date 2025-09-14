#!/bin/bash

echo "等待数据库启动..."
sleep 15

echo "开始初始化数据库..."
python init_database_docker.py

if [ $? -eq 0 ]; then
    echo "数据库初始化成功"
else
    echo "数据库初始化失败，但继续启动应用..."
fi

echo "启动应用..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 app_new:app