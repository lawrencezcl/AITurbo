"""
Docker环境下的数据库初始化脚本
用于创建MySQL数据库表结构
"""

import pymysql
import sys
import os
from services.config_service import ConfigService

def create_database_tables():
    """创建数据库表"""
    # 在Docker环境中，直接从环境变量获取数据库配置
    db_config = {
        'host': os.getenv('DB_HOST', 'db'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'user': os.getenv('DB_USER', 'aiturbo_user'),
        'password': os.getenv('DB_PASSWORD', 'aiturbo_password'),
        'database': os.getenv('DB_NAME', 'aiturbo')
    }
    
    try:
        # 连接到MySQL服务器
        connection = pymysql.connect(
            host=db_config['host'],
            port=int(db_config['port']),
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 创建表
            create_tables_sql = """
            CREATE TABLE IF NOT EXISTS article_history (
                id VARCHAR(50) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content_length INT DEFAULT 0,
                image_count INT DEFAULT 0,
                generated_at DATETIME,
                author VARCHAR(100),
                digest TEXT,
                content_source_url VARCHAR(500),
                status VARCHAR(20) DEFAULT 'generated',
                media_id VARCHAR(100),
                publish_id VARCHAR(100),
                msg_data_id VARCHAR(100),
                publish_time DATETIME NULL,
                published_at DATETIME NULL,
                saved_at DATETIME NULL,
                mass_sent BOOLEAN DEFAULT FALSE,
                mass_msg_id VARCHAR(100),
                mass_sent_at DATETIME NULL,
                enable_mass_send BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            
            CREATE TABLE IF NOT EXISTS publish_history (
                id VARCHAR(50) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                media_id VARCHAR(100),
                publish_id VARCHAR(100),
                msg_data_id VARCHAR(100),
                published_at DATETIME,
                author VARCHAR(100),
                content_length INT DEFAULT 0,
                image_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            
            CREATE TABLE IF NOT EXISTS scheduled_jobs (
                id VARCHAR(100) PRIMARY KEY,
                media_id VARCHAR(100) NOT NULL,
                publish_time DATETIME NOT NULL,
                enable_mass_send BOOLEAN DEFAULT FALSE,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            
            # 分割并执行每个SQL语句
            for statement in create_tables_sql.split(';'):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
            
            connection.commit()
            print("所有数据表创建成功")
        
        connection.close()
        print("数据库初始化完成")
        return True
        
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        return False

if __name__ == "__main__":
    if create_database_tables():
        print("数据库初始化成功")
        sys.exit(0)
    else:
        print("数据库初始化失败")
        sys.exit(1)