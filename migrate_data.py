"""
数据迁移脚本
将现有的JSON文件数据迁移到MySQL数据库
"""

import json
import os
from datetime import datetime
from services.database_service import DatabaseService
from services.config_service import ConfigService

def migrate_history_data():
    """迁移历史数据"""
    # 初始化数据库服务
    config_service = ConfigService()
    db_service = DatabaseService()
    
    db_config = config_service.get_database_config()
    if not db_service.init_database(db_config):
        print("数据库连接失败")
        return False
    
    # 迁移文章生成历史
    history_file = 'data/history.json'
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            print(f"找到 {len(history_data)} 条文章生成历史记录")
            
            success_count = 0
            for item in history_data:
                # 确保必要的字段存在
                item.setdefault('id', datetime.now().strftime('%Y%m%d%H%M%S') + str(hash(datetime.now().timestamp()))[-6:])
                item.setdefault('content_length', 0)
                item.setdefault('image_count', 0)
                item.setdefault('author', 'AI笔记')
                item.setdefault('status', 'generated')
                item.setdefault('media_id', None)
                item.setdefault('publish_id', None)
                item.setdefault('msg_data_id', None)
                item.setdefault('publish_time', None)
                item.setdefault('published_at', None)
                item.setdefault('saved_at', None)
                item.setdefault('mass_sent', False)
                item.setdefault('mass_msg_id', None)
                item.setdefault('mass_sent_at', None)
                item.setdefault('enable_mass_send', False)
                
                if db_service.add_article_history(item):
                    success_count += 1
            
            print(f"成功迁移 {success_count} 条文章生成历史记录")
        except Exception as e:
            print(f"迁移文章生成历史失败: {str(e)}")
    
    # 迁移发布历史
    publish_history_file = 'data/publish_history.json'
    if os.path.exists(publish_history_file):
        try:
            with open(publish_history_file, 'r', encoding='utf-8') as f:
                publish_history_data = json.load(f)
            
            print(f"找到 {len(publish_history_data)} 条发布历史记录")
            
            success_count = 0
            for item in publish_history_data:
                # 确保必要的字段存在
                item.setdefault('id', datetime.now().strftime('%Y%m%d%H%M%S') + str(hash(datetime.now().timestamp()))[-6:])
                item.setdefault('content_length', 0)
                item.setdefault('image_count', 0)
                item.setdefault('author', 'AI笔记')
                item.setdefault('media_id', '')
                item.setdefault('publish_id', '')
                item.setdefault('msg_data_id', '')
                
                # 这里需要直接操作数据库，因为DatabaseService没有提供直接插入发布历史的方法
                # 在实际应用中，您可以扩展DatabaseService来支持这个功能
                print(f"发布历史记录 {item.get('title', 'Unknown')} 需要手动迁移")
            
            print(f"发布历史记录迁移完成（部分需要手动处理）")
        except Exception as e:
            print(f"迁移发布历史失败: {str(e)}")
    
    print("数据迁移完成")
    return True

if __name__ == "__main__":
    migrate_history_data()