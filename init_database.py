"""
数据库初始化脚本
用于创建MySQL数据库和表结构
"""

import pymysql
import sys
import os
from services.config_service import ConfigService

def create_database():
    """创建数据库"""
    config_service = ConfigService()
    db_config = config_service.get_database_config()
    
    # 检查是否在Docker环境中运行
    is_docker = os.getenv('DOCKER_ENV', False)
    
    if is_docker:
        # 在Docker环境中，直接连接数据库创建表
        return create_database_tables(db_config)
    else:
        # 在非Docker环境中，使用root用户创建数据库
        return create_database_with_root(db_config)

def create_database_with_root(db_config):
    """使用root用户创建数据库"""
    # 使用root用户创建数据库（需要root权限）
    root_config = {
        'host': db_config['host'],
        'port': int(db_config['port']),
        'user': 'root',  # 使用root用户
        'password': input("请输入MySQL root用户密码: "),
        'charset': 'utf8mb4'
    }
    
    try:
        # 连接到MySQL服务器
        connection = pymysql.connect(
            host=root_config['host'],
            port=root_config['port'],
            user=root_config['user'],
            password=root_config['password'],
            charset=root_config['charset']
        )
        
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"数据库 {db_config['database']} 创建成功")
            
            # 创建用户并授权
            if db_config['user'] != 'root':
                cursor.execute(f"CREATE USER IF NOT EXISTS '{db_config['user']}'@'%' IDENTIFIED BY '{db_config['password']}'")
                cursor.execute(f"GRANT ALL PRIVILEGES ON {db_config['database']}.* TO '{db_config['user']}'@'%'")
                cursor.execute("FLUSH PRIVILEGES")
                print(f"用户 {db_config['user']} 创建并授权成功")
        
        connection.close()
        
        # 测试连接
        test_connection = pymysql.connect(
            host=db_config['host'],
            port=int(db_config['port']),
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            charset='utf8mb4'
        )
        
        success = create_database_tables_for_connection(test_connection)
        test_connection.close()
        
        return success
        
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        return False

def create_database_tables(db_config):
    """创建数据库表"""
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
        
        success = create_database_tables_for_connection(connection)
        connection.close()
        
        return success
        
    except Exception as e:
        print(f"数据库表创建失败: {str(e)}")
        return False

def create_database_tables_for_connection(connection):
    """为连接创建数据库表"""
    try:
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
        
        print("数据库初始化完成")
        return True
        
    except Exception as e:
        print(f"数据库表创建失败: {str(e)}")
        return False

if __name__ == "__main__":
    if create_database():
        print("数据库初始化成功")
        sys.exit(0)
    else:
        print("数据库初始化失败")
        sys.exit(1)