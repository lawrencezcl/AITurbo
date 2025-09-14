# Docker Compose 部署指南

## 概述

本指南介绍了如何使用 Docker Compose 部署 AITurbo 应用。该部署方案包含以下组件：

1. MySQL 8.0 数据库服务
2. AITurbo Python 应用服务

## 目录结构

```
AITurbo/
├── docker-compose.yml      # Docker Compose 配置文件
├── Dockerfile              # 应用镜像构建文件
├── .env.example            # 环境变量配置示例
├── init_database_docker.py # Docker环境数据库初始化脚本
└── ...                     # 其他应用文件
```

## 部署步骤

### 1. 克隆项目代码

```bash
git clone https://github.com/wojiadexiaoming/AITurbo.git
cd AITurbo
```

### 2. 配置环境变量

复制环境变量示例文件并根据需要进行修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填写必要的配置信息：

```bash
# 数据库配置
DB_HOST=db
DB_PORT=3306
DB_USER=aiturbo_user
DB_PASSWORD=aiturbo_password
DB_NAME=aiturbo

# 微信公众号配置
WECHAT_APPID=your_wechat_appid
WECHAT_APPSECRET=your_wechat_appsecret

# AI服务配置
GEMINI_API_KEY=your_gemini_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
DASHSCOPE_API_KEY=your_dashscope_api_key
PEXELS_API_KEY=your_pexels_api_key

# 其他配置
AUTHOR=AI笔记
CONTENT_SOURCE_URL=
```

### 3. 构建并启动服务

使用 Docker Compose 构建并启动所有服务：

```bash
docker-compose up -d
```

这将：
1. 构建 AITurbo 应用镜像
2. 启动 MySQL 数据库服务
3. 启动 AITurbo 应用服务

### 4. 访问应用

应用启动后，可以通过以下地址访问：

```
http://localhost:5000
```

## 服务说明

### MySQL 数据库服务

- **镜像**: mysql:8.0
- **端口**: 3306
- **数据库**: aiturbo
- **用户**: aiturbo_user
- **密码**: aiturbo_password
- **数据持久化**: 使用 Docker Volume 存储数据库文件

### AITurbo 应用服务

- **基础镜像**: python:3.11-slim
- **端口**: 5000
- **工作目录**: /app
- **依赖**: 通过 requirements.txt 安装
- **启动命令**: 使用 gunicorn 启动 Flask 应用

## 数据持久化

Docker Compose 配置了以下数据持久化：

1. **数据库数据**: 使用 Docker Volume `db_data` 存储 MySQL 数据
2. **应用数据**: 挂载本地目录到容器：
   - `./cache` → `/app/cache` (文章缓存)
   - `./data` → `/app/data` (数据文件)
   - `./logs` → `/app/logs` (日志文件)

## 管理命令

### 查看服务状态

```bash
docker-compose ps
```

### 查看服务日志

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs app
docker-compose logs db
```

### 停止服务

```bash
docker-compose down
```

### 重新构建并启动服务

```bash
docker-compose up -d --build
```

### 进入容器

```bash
# 进入应用容器
docker-compose exec app bash

# 进入数据库容器
docker-compose exec db bash
```

## 数据库管理

### 连接数据库

使用以下信息连接到 MySQL 数据库：

- **主机**: localhost
- **端口**: 3306
- **数据库**: aiturbo
- **用户**: aiturbo_user
- **密码**: aiturbo_password

### 备份数据库

```bash
docker-compose exec db mysqldump -u aiturbo_user -p aiturbo > backup.sql
```

### 恢复数据库

```bash
docker-compose exec db mysql -u aiturbo_user -p aiturbo < backup.sql
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DB_HOST | 数据库主机地址 | db |
| DB_PORT | 数据库端口 | 3306 |
| DB_USER | 数据库用户名 | aiturbo_user |
| DB_PASSWORD | 数据库密码 | aiturbo_password |
| DB_NAME | 数据库名称 | aiturbo |
| WECHAT_APPID | 微信公众号AppID |  |
| WECHAT_APPSECRET | 微信公众号AppSecret |  |
| GEMINI_API_KEY | Gemini API密钥 |  |
| DEEPSEEK_API_KEY | DeepSeek API密钥 |  |
| DASHSCOPE_API_KEY | 阿里云百炼API密钥 |  |
| PEXELS_API_KEY | Pexels API密钥 |  |
| AUTHOR | 文章作者名 | AI笔记 |
| CONTENT_SOURCE_URL | 文章来源URL |  |

## 故障排除

### 服务启动失败

1. 检查 Docker 是否正常运行
2. 查看服务日志：`docker-compose logs`
3. 确认端口未被占用

### 数据库连接失败

1. 检查数据库服务是否正常启动
2. 确认环境变量配置正确
3. 检查数据库用户权限

### 应用无法访问

1. 检查应用服务是否正常启动
2. 确认端口映射正确
3. 检查防火墙设置

## 自定义配置

### 修改端口

在 `docker-compose.yml` 中修改端口映射：

```yaml
ports:
  - "8080:5000"  # 将主机端口改为8080
```

### 修改资源限制

在 `docker-compose.yml` 中添加资源限制：

```yaml
app:
  # ... 其他配置
  deploy:
    resources:
      limits:
        memory: 512M
        cpus: '0.5'
```

### 使用外部数据库

如果要使用外部 MySQL 数据库，可以移除 `db` 服务，并在环境变量中配置外部数据库连接信息。

## 更新应用

### 拉取最新代码

```bash
git pull origin main
```

### 重新构建并重启服务

```bash
docker-compose down
docker-compose up -d --build
```

## 安全建议

1. 修改默认数据库密码
2. 不要在 `.env` 文件中存储敏感信息
3. 使用 HTTPS 访问应用
4. 定期备份数据库
5. 限制 Docker 容器的资源使用