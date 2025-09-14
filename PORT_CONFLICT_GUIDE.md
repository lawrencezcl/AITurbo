# 🔌 端口冲突解决指南

## 🚨 问题症状
```
ports are not available: exposing port TCP 0.0.0.0:5000
bind: address already in use
```

## ✅ 问题已解决！

您的应用现在运行在 **8080端口**，因为5000端口被系统程序占用。

### 🌐 新的访问地址
```
http://localhost:8080
```

## 🔍 端口占用情况

通过检查发现5000端口被以下程序占用：
```
ControlCenter (macOS 系统进程)
```

这是macOS系统的AirPlay接收器服务，通常不建议关闭。

## 🛠️ 解决方案说明

### 已自动修复：
1. **更改端口映射**: `5000:5000` → `8080:5000`
2. **更新配置文件**: docker-compose.yml
3. **更新脚本**: 所有相关脚本已更新新端口
4. **验证服务**: 应用正常运行在8080端口

## 🚀 服务状态

当前服务运行状态：
```
✅ 数据库: localhost:3306 (运行中)
✅ 应用: localhost:8080 (运行中)
✅ 健康检查: 通过
✅ HTTP响应: 200 OK
```

## 🔧 如果需要使用其他端口

### 手动修改端口：
1. 编辑 `docker-compose.yml`
2. 修改端口映射：
   ```yaml
   ports:
     - "您的端口:5000"  # 例如: "8081:5000"
   ```
3. 重启服务：
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### 使用自动端口检测脚本：
```bash
./fix_port_conflict.sh
```

## 📋 常用端口检查

### 检查端口占用：
```bash
# 检查特定端口
lsof -i :端口号

# 检查常用端口
lsof -i :5000
lsof -i :8080
lsof -i :8081
```

### 常见端口冲突：
- **5000**: macOS AirPlay, Python Flask默认端口
- **3000**: Node.js开发服务器
- **8080**: 各种Web服务器, Tomcat
- **8000**: Django默认端口

## 🔄 如果想恢复5000端口

### 方法1: 关闭AirPlay接收器（不推荐）
1. 系统偏好设置 → 共享
2. 取消勾选"隔空播放接收器"

### 方法2: 保持8080端口（推荐）
继续使用8080端口，这是更安全的选择。

## 🌐 访问应用

### Web界面：
```
http://localhost:8080
```

### API端点：
```
http://localhost:8080/api/config
http://localhost:8080/api/test-wechat
http://localhost:8080/api/generate-article
```

## 🔍 验证服务

### 快速检查：
```bash
# 检查服务状态
docker-compose ps

# 检查应用响应
curl http://localhost:8080

# 查看日志
docker-compose logs -f
```

### 详细测试：
1. 打开浏览器访问 `http://localhost:8080`
2. 检查页面是否正常加载
3. 测试配置功能
4. 验证API接口

## 💡 最佳实践

1. **使用非标准端口**: 避免与系统服务冲突
2. **文档端口**: 在项目文档中明确标注使用的端口
3. **端口检查**: 部署前检查端口可用性
4. **配置灵活性**: 使用环境变量配置端口

---

🎉 **恭喜！您的AITurbo应用已成功部署在8080端口！**

立即访问: http://localhost:8080