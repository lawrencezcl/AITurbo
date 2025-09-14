# 🚨 中国大陆网络问题快速修复

## 问题分析
您遇到的问题是Docker无法从官方镜像仓库拉取镜像。这在中国大陆是常见问题。

## 🔧 立即修复步骤

### 步骤1: 配置Docker镜像加速（必须！）

#### macOS Docker Desktop:
1. **打开Docker Desktop应用**
2. **点击右上角齿轮图标** ⚙️ 
3. **选择"Docker Engine"**
4. **将配置替换为以下内容**:
```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://dockerproxy.com",
    "https://docker.nju.edu.cn"
  ],
  "insecure-registries": [],
  "debug": false,
  "experimental": false
}
```
5. **点击"Apply & Restart"**
6. **等待Docker重启完成**

### 步骤2: 验证配置
```bash
# 检查镜像加速是否生效
docker info | grep -A 10 "Registry Mirrors"

# 测试拉取镜像
docker pull hello-world
```

### 步骤3: 重新部署
```bash
cd /Users/chenglinzhang/Desktop/AITurbo

# 清理旧容器
docker-compose down --remove-orphans

# 重新构建
docker-compose up -d --build
```

## 🎯 一键修复脚本
```bash
# 使用项目提供的修复脚本
./fix_china_network.sh
```

## 🆘 如果仍然失败

### 方案1: 手动拉取镜像
```bash
# 手动拉取所需镜像
docker pull mysql:8.0
docker pull python:3.11-slim

# 然后重新启动
docker-compose up -d
```

### 方案2: 使用科学上网
如果有科学上网工具，可以：
1. 开启代理
2. 配置Docker使用代理
3. 重新拉取镜像

### 方案3: 使用移动热点
有时移动网络比固定宽带更稳定：
1. 开启手机热点
2. 连接热点网络
3. 重新尝试部署

### 方案4: 更换DNS
```bash
# 临时更换DNS（需要管理员权限）
# 8.8.8.8 (Google DNS)
# 114.114.114.114 (国内DNS)
```

## 💡 常见错误解决

### 错误: "pull access denied"
- **原因**: 镜像仓库访问受限
- **解决**: 配置Docker镜像加速（步骤1）

### 错误: "context deadline exceeded"
- **原因**: 网络超时
- **解决**: 检查网络连接，配置镜像加速

### 错误: "repository does not exist"
- **原因**: 镜像路径错误或仓库不可用
- **解决**: 使用官方镜像路径（已修复）

## 🔍 验证部署成功
```bash
# 检查服务状态
docker-compose ps

# 查看日志
docker-compose logs

# 访问应用
curl http://localhost:5000
# 或在浏览器打开 http://localhost:5000
```

## 📞 获取帮助
如果问题仍然存在：
1. 查看详细部署指南: `CHINA_DEPLOYMENT_GUIDE.md`
2. 运行配置检查: `python3 check_setup.py`
3. 查看容器日志: `docker-compose logs -f`

---
💡 **提示**: 配置Docker镜像加速是解决问题的关键步骤，请务必完成！