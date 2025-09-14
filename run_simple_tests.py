#!/usr/bin/env python3
"""
简化测试运行脚本
"""

import sys
import os
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_simple_tests():
    """运行简化测试"""
    print("🚀 开始运行AITurbo简化测试...")
    print("=" * 50)
    
    # 只运行配置测试和基本服务测试
    try:
        from tests.test_config import TestConfigService
        from tests.test_services import TestServices
        
        # 创建测试套件
        loader = unittest.TestLoader()
        suite1 = loader.loadTestsFromTestCase(TestConfigService)
        suite2 = loader.loadTestsFromTestCase(TestServices)
        suite = unittest.TestSuite([suite1, suite2])
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # 输出测试结果统计
        print("\n" + "=" * 50)
        print("📊 测试结果统计:")
        print(f"运行测试数: {result.testsRun}")
        print(f"失败数: {len(result.failures)}")
        print(f"错误数: {len(result.errors)}")
        print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "0%")
        
        return len(result.failures) == 0 and len(result.errors) == 0
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False

if __name__ == '__main__':
    success = run_simple_tests()
    sys.exit(0 if success else 1)