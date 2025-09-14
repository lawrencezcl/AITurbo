# AITurbo Docker 本地部署指南

## 前置要求

### 1. 安装Docker

#### macOS
1. 访问 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. 下载并安装Docker Desktop
3. 启动Docker Desktop应用
4. 验证安装：
   ```bash
   docker --version
   docker-compose --version
   ```

#### Windows
1. 访问 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. 下载并安装Docker Desktop
3. 启动Docker Desktop应用
4. 验证安装：
   ```bash
   docker --version
   docker-compose --version
   ```

#### Linux (Ubuntu/Debian)
```bash
# 更新包索引
sudo apt-get update

# 安装必要的包
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

# 添加Docker的官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 设置稳定版仓库
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

## 2. 项目配置

### 2.1 环境变量配置

项目已经为您创建了 `.env` 文件，请编辑并填入您的配置：

```bash
# 编辑配置文件
vi .env
```

需要配置的重要参数：
- `WECHAT_APPID`: 微信公众号AppID
- `WECHAT_APPSECRET`: 微信公众号AppSecret  
- `GEMINI_API_KEY`: Google Gemini API密钥
- `DEEPSEEK_API_KEY`: DeepSeek API密钥
- `DASHSCOPE_API_KEY`: 阿里云百炼API密钥
- `PEXELS_API_KEY`: Pexels图片API密钥

### 2.2 检查项目文件

确保以下文件存在：
- [x] `docker-compose.yml` - Docker Compose配置
- [x] `Dockerfile` - 应用镜像配置
- [x] `.env` - 环境变量配置
- [x] `requirements.txt` - Python依赖
- [x] `start_app.sh` - 应用启动脚本
- [x] `mysql/init/init.sql` - 数据库初始化脚本

## 3. 构建和运行

### 3.1 构建并启动服务

```bash
# 在项目根目录执行
cd /Users/chenglinzhang/Desktop/AITurbo

# 构建并启动所有服务
docker-compose up -d --build
```

### 3.2 查看服务状态

```bash
# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs app
docker-compose logs db
```

### 3.3 访问应用

应用启动后，在浏览器中访问：
```
http://localhost:5000
```

## 4. 故障排除

### 4.1 常见问题

#### 端口被占用
如果5000端口被占用，可以修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:5000"  # 改为8080端口
```

#### 数据库连接失败
检查数据库服务是否正常启动：
```bash
docker-compose logs db
```

#### 应用启动失败
查看应用日志：
```bash
docker-compose logs app
```

### 4.2 重新构建

如果需要重新构建：
```bash
# 停止所有服务
docker-compose down

# 删除所有容器和镜像（可选）
docker-compose down --rmi all --volumes

# 重新构建并启动
docker-compose up -d --build
```

## 5. 数据管理

### 5.1 数据持久化

数据会自动持久化到以下目录：
- `./cache` - 文章缓存
- `./data` - 数据文件  
- `./logs` - 日志文件
- `./config` - 配置文件
- Docker Volume `db_data` - 数据库数据

### 5.2 数据备份

```bash
# 备份数据库
docker-compose exec db mysqldump -u aiturbo_user -p aiturbo > backup.sql

# 恢复数据库
docker-compose exec db mysql -u aiturbo_user -p aiturbo < backup.sql
```

## 6. 开发模式

如果需要开发调试，可以使用开发模式：

```bash
# 停止应用容器但保留数据库
docker-compose stop app

# 在本地运行应用
python app_new.py
```

## 7. 清理资源

```bash
# 停止并删除所有容器
docker-compose down

# 删除所有容器、网络和未使用的镜像
docker-compose down --rmi all --volumes --remove-orphans

# 清理Docker系统（谨慎使用）
docker system prune -a
```

## 8. 监控和维护

### 8.1 查看资源使用

```bash
# 查看容器资源使用情况
docker stats

# 查看镜像大小
docker images
```

### 8.2 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 快速启动命令汇总

```bash
# 1. 安装Docker（如果未安装）
# 2. 配置.env文件
# 3. 构建并启动
docker-compose up -d --build

# 4. 查看状态
docker-compose ps

# 5. 查看日志
docker-compose logs -f

# 6. 访问应用
open http://localhost:5000
```