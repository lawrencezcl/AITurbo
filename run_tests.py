#!/usr/bin/env python3
"""
测试运行脚本
"""

import sys
import os
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    """运行所有测试"""
    print("🚀 开始运行AITurbo测试套件...")
    print("=" * 50)
    
    # 发现并运行测试
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test*.py')
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试结果统计
    print("\n" + "=" * 50)
    print("📊 测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "0%")
    
    # 详细失败信息
    if result.failures:
        print("\n❌ 失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    # 返回测试结果
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)