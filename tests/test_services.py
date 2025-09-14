"""
服务模块测试
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestServices(unittest.TestCase):
    """服务模块测试类"""
    
    def test_config_service_methods(self):
        """测试配置服务方法"""
        try:
            from services.config_service import ConfigService
            
            # 创建配置服务实例
            config_service = ConfigService()
            
            # 测试方法是否存在
            methods_to_test = [
                'load_config',
                'save_config',
                'get_config_value',
                'set_config_value',
                'get_wechat_config',
                'get_gemini_config',
                'get_deepseek_config',
                'get_dashscope_config',
                'get_pexels_config',
                'get_author_config',
                'get_database_config',
                'is_wechat_configured',
                'is_gemini_configured',
                'is_deepseek_configured',
                'is_dashscope_configured',
                'is_pexels_configured',
                'is_database_configured',
                'get_config_status'
            ]
            
            for method_name in methods_to_test:
                self.assertTrue(
                    hasattr(config_service, method_name),
                    f"配置服务缺少方法: {method_name}"
                )
            
            print("✓ 配置服务所有方法检查通过")
        except Exception as e:
            self.fail(f"配置服务方法测试失败: {e}")
    
    def test_prompt_manager_import(self):
        """测试提示管理器导入"""
        try:
            from services.prompt_manager import PromptManager
            prompt_manager = PromptManager()
            self.assertIsNotNone(prompt_manager)
            print("✓ 提示管理器导入成功")
        except Exception as e:
            self.fail(f"提示管理器导入失败: {e}")
    
    def test_history_service_import(self):
        """测试历史服务导入"""
        try:
            from services.history_service import HistoryService
            history_service = HistoryService()
            self.assertIsNotNone(history_service)
            print("✓ 历史服务导入成功")
        except Exception as e:
            self.fail(f"历史服务导入失败: {e}")
    
    def test_draft_service_import(self):
        """测试草稿服务导入"""
        try:
            from services.draft_service import DraftService
            draft_service = DraftService()
            self.assertIsNotNone(draft_service)
            print("✓ 草稿服务导入成功")
        except Exception as e:
            self.fail(f"草稿服务导入失败: {e}")
    
    def test_image_service_import(self):
        """测试图像服务导入"""
        try:
            from services.image_service import ImageService
            image_service = ImageService()
            self.assertIsNotNone(image_service)
            print("✓ 图像服务导入成功")
        except Exception as e:
            self.fail(f"图像服务导入失败: {e}")

if __name__ == '__main__':
    unittest.main()