# 🧠 Docker内存不足问题解决指南

## 🚨 问题症状
```
ResourceExhausted: cannot allocate memory
process did not complete successfully
```

## 🔧 立即解决方案

### 方案1: 调整Docker Desktop内存（推荐）

#### macOS/Windows Docker Desktop:
1. **打开Docker Desktop**
2. **点击设置** ⚙️
3. **选择 Resources → Advanced**
4. **调整内存分配**:
   - 最小: 4GB
   - 推荐: 6-8GB
5. **点击 "Apply & Restart"**
6. **等待Docker重启完成**

### 方案2: 使用内存优化脚本
```bash
cd /Users/chenglinzhang/Desktop/AITurbo

# 运行内存优化脚本
./fix_memory_issue.sh
```

### 方案3: 手动使用轻量级构建
```bash
# 使用Alpine Linux版本（更轻量）
cp Dockerfile.lightweight Dockerfile

# 清理缓存
docker system prune -f
docker builder prune -f

# 重新构建
docker-compose build --memory=2g
docker-compose up -d
```

## 🔍 内存使用优化

### 已优化的配置:
1. **减少worker进程**: 从4个减少到2个
2. **限制容器内存**: 应用1GB，数据库512MB
3. **MySQL优化**: 减少缓冲池大小
4. **分批安装**: Python包分批安装减少内存峰值

### 当前资源配置:
```yaml
app:
  memory: 1GB (限制)
  workers: 2个
  
db:
  memory: 512MB (限制)
  buffer-pool: 128MB
```

## 🚀 推荐部署步骤

### 步骤1: 检查系统资源
```bash
# 检查可用内存
free -h  # Linux
vm_stat  # macOS

# 检查Docker资源
docker system df
docker stats
```

### 步骤2: 调整Docker设置
- **内存**: 至少4GB，推荐6-8GB
- **CPU**: 至少2核
- **磁盘**: 至少10GB可用空间

### 步骤3: 优化构建
```bash
# 清理缓存
docker system prune -f

# 使用内存限制构建
export DOCKER_BUILDKIT=1
docker-compose build --memory=2g

# 启动服务
docker-compose up -d
```

## 🆘 其他解决方案

### 如果问题仍然存在:

#### 1. 重启系统
```bash
# 完全重启释放内存
sudo reboot
```

#### 2. 关闭其他应用
- 关闭浏览器多余标签
- 关闭IDE/编辑器
- 关闭其他Docker容器

#### 3. 使用云服务器
如果本地资源不足，可以考虑：
- 阿里云ECS（2核4G起）
- 腾讯云CVM（2核4G起）
- AWS EC2（t3.medium起）

#### 4. 分离部署
```bash
# 仅启动数据库
docker-compose up -d db

# 本地运行应用
python app_new.py
```

## 📊 监控资源使用

### 实时监控
```bash
# 监控容器资源
docker stats

# 监控具体容器
docker stats aiturbo_app aiturbo_db

# 查看内存使用详情
docker exec aiturbo_app cat /proc/meminfo
```

### 日志查看
```bash
# 查看构建日志
docker-compose logs --follow app

# 查看系统资源日志
dmesg | grep -i memory
```

## 💡 预防措施

1. **定期清理**: `docker system prune -f`
2. **监控资源**: 定期检查内存使用
3. **合理配置**: 根据机器配置调整容器资源
4. **分阶段构建**: 避免一次性安装过多依赖

## 🏃‍♂️ 快速命令汇总

```bash
# 一键修复内存问题
./fix_memory_issue.sh

# 手动修复流程
docker system prune -f
cp Dockerfile.lightweight Dockerfile
docker-compose build --memory=2g
docker-compose up -d

# 验证部署
docker-compose ps
curl http://localhost:5000
```

---
💡 **关键提示**: Docker Desktop的内存分配是解决问题的关键，请确保分配至少4GB内存！