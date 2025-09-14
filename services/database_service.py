"""
数据库服务模块
处理MySQL数据库连接和操作
"""

import logging
from typing import Dict, Any, List, Optional
import pymysql
from pymysql.connections import Connection
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        self.connection: Optional[Connection] = None
        self.db_config: Optional[Dict[str, str]] = None
        logger.info("数据库服务初始化完成")
    
    def init_database(self, db_config: Dict[str, str]) -> bool:
        """
        初始化数据库连接
        :param db_config: 数据库配置 {"host": "", "port": "", "user": "", "password": "", "database": ""}
        :return: 是否初始化成功
        """
        try:
            self.db_config = db_config
            
            # 测试数据库连接
            self.connection = pymysql.connect(
                host=db_config['host'],
                port=int(db_config['port']),
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                charset='utf8mb4',
                autocommit=True
            )
            
            # 测试连接
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            logger.info("数据库连接初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"数据库连接初始化失败: {str(e)}")
            return False
    
    def create_tables(self) -> bool:
        """
        创建数据库表
        :return: 是否创建成功
        """
        try:
            if not self.connection:
                logger.error("数据库连接未初始化")
                return False
            
            # 创建表的SQL语句
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
            
            # 执行创建表语句
            with self.connection.cursor() as cursor:
                # 分割并执行每个SQL语句
                for statement in create_tables_sql.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
            
            logger.info("数据库表创建成功")
            return True
            
        except Exception as e:
            logger.error(f"创建数据库表失败: {str(e)}")
            return False
    
    def add_article_history(self, article_data: Dict[str, Any]) -> bool:
        """
        添加文章生成历史记录
        :param article_data: 文章数据
        :return: 是否添加成功
        """
        try:
            if not self.connection:
                logger.error("数据库连接未初始化")
                return False
            
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO article_history (
                    id, title, content_length, image_count, generated_at, author, 
                    digest, content_source_url, status, media_id, publish_id, 
                    msg_data_id, publish_time, published_at, saved_at, mass_sent, 
                    mass_msg_id, mass_sent_at, enable_mass_send
                ) VALUES (
                    %(id)s, %(title)s, %(content_length)s, %(image_count)s, %(generated_at)s, %(author)s, 
                    %(digest)s, %(content_source_url)s, %(status)s, %(media_id)s, %(publish_id)s, 
                    %(msg_data_id)s, %(publish_time)s, %(published_at)s, %(saved_at)s, %(mass_sent)s, 
                    %(mass_msg_id)s, %(mass_sent_at)s, %(enable_mass_send)s
                ) ON DUPLICATE KEY UPDATE
                    title = VALUES(title),
                    content_length = VALUES(content_length),
                    image_count = VALUES(image_count),
                    author = VALUES(author),
                    digest = VALUES(digest),
                    content_source_url = VALUES(content_source_url),
                    status = VALUES(status),
                    updated_at = CURRENT_TIMESTAMP
                """
                
                cursor.execute(sql, article_data)
                self.connection.commit()
                logger.info(f"添加文章历史记录成功: {article_data.get('title', '')}")
                return True
                
        except Exception as e:
            logger.error(f"添加文章历史记录失败: {str(e)}")
            return False
    
    def update_draft_status(self, title: str, media_id: str, publish_time: Optional[str] = None) -> bool:
        """
        更新草稿保存状态
        :param title: 文章标题
        :param media_id: 微信草稿media_id
        :param publish_time: 定时发布时间（可选）
        :return: 是否更新成功
        """
        try:
            if not self.connection:
                logger.error("数据库连接未初始化")
                return False
            
            with self.connection.cursor() as cursor:
                sql = """
                UPDATE article_history 
                SET status = 'saved', 
                    media_id = %s, 
                    saved_at = NOW(),
                    publish_time = %s,
                    updated_at = NOW()
                WHERE (title = %s OR media_id = %s) AND status != 'published'
                """
                
                cursor.execute(sql, (media_id, publish_time, title, media_id))
                self.connection.commit()
                
                if cursor.rowcount > 0:
                    logger.info(f"更新草稿状态成功: {title} -> media_id: {media_id}")
                    return True
                else:
                    logger.warning(f"未找到匹配的文章历史记录: {title} 或 media_id: {media_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"更新草稿状态失败: {str(e)}")
            return False
    
    def update_publish_status(self, media_id: str, publish_data: Dict[str, Any]) -> bool:
        """
        更新发布状态
        :param media_id: 微信草稿media_id
        :param publish_data: 发布结果数据
        :return: 是否更新成功
        """
        try:
            if not self.connection:
                logger.error("数据库连接未初始化")
                return False
            
            with self.connection.cursor() as cursor:
                # 更新文章历史表
                update_sql = """
                UPDATE article_history 
                SET status = 'published', 
                    publish_id = %s, 
                    msg_data_id = %s, 
                    published_at = NOW(),
                    updated_at = NOW()
                WHERE media_id = %s AND status != 'published'
                """
                
                cursor.execute(update_sql, (
                    publish_data.get('publish_id'),
                    publish_data.get('msg_data_id'),
                    media_id
                ))
                
                # 如果更新成功，添加到发布历史表
                if cursor.rowcount > 0:
                    insert_publish_sql = """
                    INSERT INTO publish_history (
                        id, title, media_id, publish_id, msg_data_id, published_at, 
                        author, content_length, image_count
                    ) SELECT 
                        %s, title, %s, %s, %s, NOW(),
                        author, content_length, image_count
                    FROM article_history 
                    WHERE media_id = %s
                    """
                    
                    cursor.execute(insert_publish_sql, (
                        publish_data.get('publish_id', ''),
                        media_id,
                        publish_data.get('publish_id'),
                        publish_data.get('msg_data_id'),
                        media_id
                    ))
                    self.connection.commit()
                    logger.info(f"更新发布状态成功: media_id {media_id} -> publish_id {publish_data.get('publish_id')}")
                    return True
                else:
                    logger.warning(f"未找到匹配的草稿记录: media_id {media_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"更新发布状态失败: {str(e)}")
            return False
    
    def get_article_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        获取文章生成历史
        :param limit: 返回数量限制
        :return: 历史记录列表
        """
        try:
            if not self.connection:
                logger.error("数据库连接未初始化")
                return []
            
            with self.connection.cursor() as cursor:
                sql = """
                SELECT * FROM article_history 
                ORDER BY generated_at DESC 
                LIMIT %s
                """
                
                cursor.execute(sql, (limit,))
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                # 转换为字典列表
                history = []
                for row in rows:
                    history.append(dict(zip(columns, row)))
                
                return history
                
        except Exception as e:
            logger.error(f"获取文章历史失败: {str(e)}")
            return []
    
    def get_publish_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        获取发布历史
        :param limit: 返回数量限制
        :return: 发布历史列表
        """
        try:
            if not self.connection:
                logger.error("数据库连接未初始化")
                return []
            
            with self.connection.cursor() as cursor:
                sql = """
                SELECT * FROM publish_history 
                ORDER BY published_at DESC 
                LIMIT %s
                """
                
                cursor.execute(sql, (limit,))
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                # 转换为字典列表
                history = []
                for row in rows:
                    history.append(dict(zip(columns, row)))
                
                return history
                
        except Exception as e:
            logger.error(f"获取发布历史失败: {str(e)}")
            return []
    
    def add_scheduled_job(self, job_data: Dict[str, Any]) -> bool:
        """
        添加定时任务记录
        :param job_data: 任务数据
        :return: 是否添加成功
        """
        try:
            if not self.connection:
                logger.error("数据库连接未初始化")
                return False
            
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO scheduled_jobs (
                    id, media_id, publish_time, enable_mass_send, status
                ) VALUES (
                    %(id)s, %(media_id)s, %(publish_time)s, %(enable_mass_send)s, %(status)s
                ) ON DUPLICATE KEY UPDATE
                    publish_time = VALUES(publish_time),
                    enable_mass_send = VALUES(enable_mass_send),
                    status = VALUES(status),
                    updated_at = CURRENT_TIMESTAMP
                """
                
                cursor.execute(sql, job_data)
                self.connection.commit()
                logger.info(f"添加定时任务记录成功: {job_data.get('id', '')}")
                return True
                
        except Exception as e:
            logger.error(f"添加定时任务记录失败: {str(e)}")
            return False
    
    def get_pending_scheduled_jobs(self) -> List[Dict[str, Any]]:
        """
        获取待执行的定时任务
        :return: 任务列表
        """
        try:
            if not self.connection:
                logger.error("数据库连接未初始化")
                return []
            
            with self.connection.cursor() as cursor:
                sql = """
                SELECT * FROM scheduled_jobs 
                WHERE status = 'pending' AND publish_time > NOW()
                ORDER BY publish_time ASC
                """
                
                cursor.execute(sql)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                # 转换为字典列表
                jobs = []
                for row in rows:
                    jobs.append(dict(zip(columns, row)))
                
                return jobs
                
        except Exception as e:
            logger.error(f"获取定时任务失败: {str(e)}")
            return []