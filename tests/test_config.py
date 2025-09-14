"""
配置服务测试
"""

import sys
import os
import json
import tempfile
import unittest
from unittest.mock import patch, mock_open

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.config_service import ConfigService

class TestConfigService(unittest.TestCase):
    """配置服务测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.test_config = {
            "wechat_appid": "test_appid",
            "wechat_appsecret": "test_appsecret",
            "gemini_api_key": "test_gemini_key",
            "author": "Test Author",
            "db_host": "localhost",
            "db_port": "3306",
            "db_user": "test_user",
            "db_password": "test_password",
            "db_name": "test_db"
        }
        
    def test_load_config_from_file(self):
        """测试从文件加载配置"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(self.test_config, f)
            temp_file = f.name
        
        try:
            # 创建配置服务实例
            config_service = ConfigService(temp_file)
            config = config_service.load_config()
            
            # 验证配置加载
            self.assertEqual(config['wechat_appid'], 'test_appid')
            self.assertEqual(config['gemini_api_key'], 'test_gemini_key')
            self.assertEqual(config['author'], 'Test Author')
        finally:
            # 清理临时文件
            os.unlink(temp_file)
    
    def test_default_config(self):
        """测试默认配置"""
        # 使用不存在的配置文件
        config_service = ConfigService('/nonexistent/config.json')
        config = config_service.load_config()
        
        # 验证默认值
        self.assertIn('wechat_appid', config)
        self.assertIn('gemini_api_key', config)
        self.assertIn('author', config)
        self.assertEqual(config['author'], 'AI笔记')  # 默认作者
    
    def test_get_wechat_config(self):
        """测试获取微信配置"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(self.test_config, f)
            temp_file = f.name
        
        try:
            config_service = ConfigService(temp_file)
            wechat_config = config_service.get_wechat_config()
            
            self.assertEqual(wechat_config['appid'], 'test_appid')
            self.assertEqual(wechat_config['appsecret'], 'test_appsecret')
        finally:
            os.unlink(temp_file)
    
    def test_get_database_config(self):
        """测试获取数据库配置"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(self.test_config, f)
            temp_file = f.name
        
        try:
            config_service = ConfigService(temp_file)
            db_config = config_service.get_database_config()
            
            self.assertEqual(db_config['host'], 'localhost')
            self.assertEqual(db_config['user'], 'test_user')
            self.assertEqual(db_config['database'], 'test_db')
        finally:
            os.unlink(temp_file)

if __name__ == '__main__':
    unittest.main()