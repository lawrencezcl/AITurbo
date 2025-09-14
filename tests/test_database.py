"""
数据库服务测试（简化版）
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDatabaseService(unittest.TestCase):
    """数据库服务测试类（简化版）"""
    
    @patch('services.database_service.pymysql')
    def test_database_service_import(self, mock_pymysql):
        """测试数据库服务导入"""
        try:
            from services.database_service import DatabaseService
            db_service = DatabaseService()
            self.assertIsNotNone(db_service)
        except Exception as e:
            self.fail(f"数据库服务导入失败: {e}")
    
    def test_database_service_methods(self):
        """测试数据库服务方法定义"""
        # 这里我们只测试方法是否存在，不实际执行
        try:
            from services.database_service import DatabaseService
            db_service = DatabaseService()
            
            # 检查方法是否存在
            self.assertTrue(hasattr(db_service, 'init_database'))
            self.assertTrue(hasattr(db_service, 'create_tables'))
            self.assertTrue(hasattr(db_service, 'add_article_history'))
            self.assertTrue(hasattr(db_service, 'get_article_history'))
        except Exception as e:
            self.fail(f"数据库服务方法测试失败: {e}")

if __name__ == '__main__':
    unittest.main()