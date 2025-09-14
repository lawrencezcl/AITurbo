#!/usr/bin/env python3
"""
项目配置检查脚本
验证项目是否准备好进行Docker部署
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - 文件不存在")
        return False

def check_directory_exists(dir_path, description):
    """检查目录是否存在"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} - 目录不存在")
        return False

def check_env_file():
    """检查环境变量文件"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ 环境变量文件 {env_file} 不存在")
        return False
    
    print(f"✅ 环境变量文件: {env_file}")
    
    # 读取环境变量文件并检查重要配置
    important_vars = [
        'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME',
        'WECHAT_APPID', 'WECHAT_APPSECRET',
        'GEMINI_API_KEY', 'AUTHOR'
    ]
    
    env_vars = {}
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except Exception as e:
        print(f"❌ 读取环境变量文件时出错: {e}")
        return False
    
    print("\n📋 环境变量配置检查:")
    for var in important_vars:
        value = env_vars.get(var, '')
        if value:
            if var in ['WECHAT_APPID', 'WECHAT_APPSECRET', 'GEMINI_API_KEY']:
                if value.startswith('your_') or not value.strip():
                    print(f"⚠️  {var}: 需要配置实际值")
                else:
                    print(f"✅ {var}: 已配置")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 未配置")
    
    return True

def check_python_dependencies():
    """检查Python依赖文件"""
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        print(f"❌ Python依赖文件 {req_file} 不存在")
        return False
    
    print(f"✅ Python依赖文件: {req_file}")
    
    # 检查重要依赖
    important_deps = ['Flask', 'PyMySQL', 'requests', 'gunicorn']
    
    try:
        with open(req_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
        print("\n📦 重要依赖检查:")
        for dep in important_deps:
            if dep.lower() in content:
                print(f"✅ {dep}: 已包含")
            else:
                print(f"❌ {dep}: 未找到")
    except Exception as e:
        print(f"❌ 读取依赖文件时出错: {e}")
        return False
    
    return True

def main():
    """主检查函数"""
    print("🔍 AITurbo 项目配置检查")
    print("=" * 50)
    
    current_dir = os.getcwd()
    print(f"📁 当前目录: {current_dir}")
    print()
    
    # 检查文件列表
    files_to_check = [
        ("docker-compose.yml", "Docker Compose配置文件"),
        ("Dockerfile", "Docker镜像配置文件"),
        (".env.example", "环境变量示例文件"),
        ("app_new.py", "主应用文件"),
        ("start_app.sh", "应用启动脚本"),
        ("init_database_docker.py", "数据库初始化脚本"),
    ]
    
    # 检查目录列表
    dirs_to_check = [
        ("config", "配置目录"),
        ("services", "服务目录"),
        ("controllers", "控制器目录"),
        ("templates", "模板目录"),
        ("static", "静态文件目录"),
        ("mysql/init", "MySQL初始化目录"),
    ]
    
    print("📁 文件检查:")
    file_checks = []
    for file_path, description in files_to_check:
        file_checks.append(check_file_exists(file_path, description))
    
    print("\n📁 目录检查:")
    dir_checks = []
    for dir_path, description in dirs_to_check:
        dir_checks.append(check_directory_exists(dir_path, description))
    
    print("\n" + "=" * 50)
    
    # 检查环境变量文件
    env_check = check_env_file()
    
    print("\n" + "=" * 50)
    
    # 检查Python依赖
    dep_check = check_python_dependencies()
    
    print("\n" + "=" * 50)
    print("📊 检查总结:")
    
    total_checks = len(file_checks) + len(dir_checks) + 2  # +2 for env and deps
    passed_checks = sum(file_checks) + sum(dir_checks) + int(env_check) + int(dep_check)
    
    print(f"总检查项: {total_checks}")
    print(f"通过检查: {passed_checks}")
    print(f"失败检查: {total_checks - passed_checks}")
    
    if passed_checks == total_checks:
        print("🎉 所有检查都通过！项目准备好进行Docker部署。")
        print("\n🚀 下一步:")
        print("1. 确保Docker已安装并运行")
        print("2. 配置.env文件中的API密钥")
        print("3. 运行: docker-compose up -d --build")
        return True
    else:
        print("⚠️  存在一些问题需要解决。")
        print("\n🔧 建议:")
        print("1. 检查缺失的文件和目录")
        print("2. 确保.env文件配置正确")
        print("3. 查看DOCKER_SETUP_GUIDE.md获取详细指导")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)