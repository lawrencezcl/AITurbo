# 中国大陆Docker部署指南

## 🇨🇳 针对中国大陆用户的优化配置

### 1. Docker镜像加速配置

#### macOS Docker Desktop配置
1. 打开Docker Desktop
2. 点击右上角设置图标 ⚙️
3. 选择"Docker Engine"
4. 替换配置内容为：
```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://registry.cn-hangzhou.aliyuncs.com"
  ],
  "insecure-registries": [],
  "debug": false,
  "experimental": false
}
```
5. 点击"Apply & Restart"

#### Linux系统配置
```bash
# 创建docker配置目录
sudo mkdir -p /etc/docker

# 创建配置文件
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://registry.cn-hangzhou.aliyuncs.com"
  ]
}
EOF

# 重启Docker服务
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 2. 验证镜像加速
```bash
# 查看Docker配置
docker info | grep -A 10 "Registry Mirrors"

# 测试拉取镜像
docker pull hello-world
```

### 3. 使用优化后的配置

项目已经为您配置了以下优化：

1. **Docker镜像源优化**:
   - MySQL: `registry.cn-hangzhou.aliyuncs.com/library/mysql:8.0`
   - Python: `registry.cn-hangzhou.aliyuncs.com/library/python:3.11-slim`

2. **APT软件源优化**:
   - 使用阿里云镜像源替换默认Debian源

3. **Python包管理优化**:
   - 使用清华大学PyPI镜像源: `https://pypi.tuna.tsinghua.edu.cn/simple`

### 4. 快速部署步骤

```bash
# 1. 确保Docker已配置镜像加速
# 2. 进入项目目录
cd /Users/chenglinzhang/Desktop/AITurbo

# 3. 清理之前的容器（如果有）
docker-compose down --remove-orphans

# 4. 清理Docker缓存（可选）
docker system prune -f

# 5. 构建并启动服务
docker-compose up -d --build

# 6. 查看启动状态
docker-compose ps

# 7. 查看日志
docker-compose logs -f
```

### 5. 故障排除

#### 问题1: 镜像拉取超时
```bash
# 解决方案1: 手动拉取镜像
docker pull registry.cn-hangzhou.aliyuncs.com/library/mysql:8.0
docker pull registry.cn-hangzhou.aliyuncs.com/library/python:3.11-slim

# 解决方案2: 使用不同的镜像源
# 编辑docker-compose.yml，替换为其他镜像源
```

#### 问题2: Python包安装失败
```bash
# 在Dockerfile中尝试其他PyPI镜像
pip install -i https://pypi.douban.com/simple -r requirements.txt
# 或者
pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
```

#### 问题3: 网络连接问题
```bash
# 检查网络连接
ping docker.mirrors.ustc.edu.cn
ping registry.cn-hangzhou.aliyuncs.com

# 如果仍有问题，可以尝试使用VPN或代理
```

### 6. 推荐的镜像源

#### Docker镜像源（按推荐顺序）
1. 🏛️ **中科大镜像**: `https://docker.mirrors.ustc.edu.cn`
2. 🔵 **网易镜像**: `https://hub-mirror.c.163.com`
3. 🟡 **百度镜像**: `https://mirror.baidubce.com`
4. 🟠 **阿里云镜像**: `https://registry.cn-hangzhou.aliyuncs.com`

#### Python包管理源
1. 🏛️ **清华大学**: `https://pypi.tuna.tsinghua.edu.cn/simple`
2. 🔵 **豆瓣**: `https://pypi.douban.com/simple`
3. 🟠 **阿里云**: `https://mirrors.aliyun.com/pypi/simple`
4. 🏛️ **中科大**: `https://pypi.mirrors.ustc.edu.cn/simple`

### 7. 性能优化建议

1. **使用SSD存储**: Docker容器和镜像存储在SSD上
2. **分配足够内存**: 建议至少4GB RAM给Docker
3. **定期清理**: `docker system prune` 清理无用镜像和容器
4. **使用本地缓存**: 避免重复下载相同的依赖包

### 8. 网络优化

如果仍然遇到网络问题，可以考虑：

1. **使用科学上网工具**
2. **配置HTTP代理**:
```bash
# 在~/.docker/config.json中配置代理
{
  "proxies": {
    "default": {
      "httpProxy": "http://proxy.example.com:8080",
      "httpsProxy": "http://proxy.example.com:8080"
    }
  }
}
```

3. **使用移动热点**: 有时移动网络比固定宽带更稳定

### 9. 完整部署命令

```bash
# 一键部署脚本（复制整段执行）
cd /Users/chenglinzhang/Desktop/AITurbo && \
docker-compose down --remove-orphans && \
docker system prune -f && \
echo "开始构建，请耐心等待..." && \
docker-compose up -d --build && \
echo "部署完成！" && \
docker-compose ps && \
echo "访问地址: http://localhost:5000"
```

---

💡 **提示**: 如果首次构建时间较长，这是正常现象，Docker需要下载基础镜像和安装依赖。后续启动会很快。