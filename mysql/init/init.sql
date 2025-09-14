-- 创建数据库表
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