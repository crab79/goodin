-- ====================================================
-- 股引 GOODIN 學習平台資料庫架構
-- 建立日期: 2025-01-20
-- 說明: 純粹的資料庫架構，不包含任何測試資料
-- ====================================================

-- 建立資料庫
CREATE DATABASE IF NOT EXISTS goodin_learning_platform 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE goodin_learning_platform;

-- ====================================================
-- 1. 用戶資料表
-- ====================================================
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    real_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(255),
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    user_role ENUM('student', 'instructor', 'admin') DEFAULT 'student',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_active_users (is_active, user_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 2. 課程資料表
-- ====================================================
CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    course_order INT NOT NULL COMMENT '課程順序',
    category ENUM('introduction', 'technical_analysis', 'fundamental_analysis', 'trading_strategy') DEFAULT 'technical_analysis',
    thumbnail_url VARCHAR(255),
    video_url VARCHAR(255),
    content_text TEXT,
    learning_objectives JSON COMMENT '學習目標 (JSON 格式)',
    prerequisites JSON COMMENT '先修條件 (課程ID列表)',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_course_order (course_order),
    INDEX idx_category (category),
    INDEX idx_active_courses (is_active, course_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 3. 課程頁面內容表 (對應 course1_api.py 的頁面資料)
-- ====================================================
CREATE TABLE course_pages (
    page_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    page_index INT NOT NULL COMMENT '頁面順序索引',
    html_content LONGTEXT NOT NULL COMMENT '頁面HTML內容',
    chart_type VARCHAR(50) COMMENT '圖表類型',
    chart_config JSON COMMENT '圖表配置 (JSON格式)',
    multi_steps JSON COMMENT '多步驟顯示元素ID列表 (JSON格式)',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_course_page (course_id, page_index),
    INDEX idx_course_pages (course_id, page_index),
    INDEX idx_active_pages (is_active, course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 4. 用戶課程進度表
-- ====================================================
CREATE TABLE user_course_progress (
    progress_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    status ENUM('not_started', 'in_progress', 'completed') DEFAULT 'not_started',
    started_at DATETIME,
    completed_at DATE,
    last_accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    watch_duration_seconds INT DEFAULT 0 COMMENT '觀看時間(秒)',
    completion_percentage DECIMAL(5,2) DEFAULT 0 COMMENT '完成百分比',
    notes TEXT COMMENT '用戶筆記',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_course (user_id, course_id),
    INDEX idx_user_progress (user_id, status),
    INDEX idx_course_progress (course_id),
    INDEX idx_completed_courses (user_id, completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 5. 練習題目庫
-- ====================================================
CREATE TABLE questions (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    question_type ENUM('multiple_choice', 'true_false', 'chart_analysis', 'drag_drop') DEFAULT 'multiple_choice',
    question_number INT NOT NULL COMMENT '題目編號',
    question_text TEXT NOT NULL,
    question_description TEXT COMMENT '題目說明',
    image_url VARCHAR(255) COMMENT '圖片URL (如K線圖)',
    chart_data JSON COMMENT '圖表資料 (JSON格式)',
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    explanation TEXT COMMENT '解答說明',
    points INT DEFAULT 1 COMMENT '題目分數',
    tags JSON COMMENT '標籤 (JSON格式)',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    INDEX idx_course_questions (course_id, question_number),
    INDEX idx_question_type (question_type),
    INDEX idx_difficulty (difficulty),
    INDEX idx_active_questions (is_active, course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 6. 題目選項表
-- ====================================================
CREATE TABLE question_options (
    option_id INT PRIMARY KEY AUTO_INCREMENT,
    question_id INT NOT NULL,
    option_code CHAR(1) NOT NULL COMMENT '選項代碼 (A, B, C, D)',
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    option_order INT NOT NULL,
    explanation TEXT COMMENT '選項解釋',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    INDEX idx_question_options (question_id, option_order),
    INDEX idx_correct_options (question_id, is_correct)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 7. 練習活動表 (對應 fake_user_practice_progress)
-- ====================================================
CREATE TABLE practice_sessions (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    exercise_id INT NOT NULL COMMENT '對應原始的 exercise_id',
    course_id INT NOT NULL,
    session_type ENUM('course_practice', 'review_practice', 'exam', 'choice', 'chart') DEFAULT 'course_practice',
    title VARCHAR(200) NOT NULL COMMENT '練習標題',
    total_questions INT NOT NULL,
    correct_answers INT NOT NULL,
    wrong_answers INT NOT NULL,
    accuracy_rate DECIMAL(5,2) NOT NULL COMMENT '正確率百分比',
    total_score INT DEFAULT 0,
    max_possible_score INT DEFAULT 0,
    started_at DATETIME,
    completed_at DATETIME NOT NULL,
    duration_seconds INT COMMENT '總作答時間(秒)',
    exercise_type ENUM('choice', 'chart') DEFAULT 'choice',
    ip_address VARCHAR(45),
    user_agent TEXT,
    is_completed BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    INDEX idx_user_sessions (user_id, completed_at),
    INDEX idx_course_sessions (course_id),
    INDEX idx_session_date (completed_at),
    INDEX idx_exercise_sessions (exercise_id, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 8. 用戶答題記錄表
-- ====================================================
CREATE TABLE user_answers (
    answer_id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    question_number INT COMMENT '題目編號',
    selected_option_id INT,
    selected_option_code CHAR(1),
    user_answer_text TEXT COMMENT '用戶輸入的答案文字',
    is_correct BOOLEAN NOT NULL,
    answer_duration_seconds INT COMMENT '單題作答時間(秒)',
    answered_at DATETIME COMMENT '答題時間',
    score_earned INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES practice_sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    FOREIGN KEY (selected_option_id) REFERENCES question_options(option_id) ON DELETE SET NULL,
    INDEX idx_session_answers (session_id),
    INDEX idx_user_answers (user_id, answered_at),
    INDEX idx_question_stats (question_id, is_correct)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 9. 錯題記錄表 (對應 fake_practice_errors)
-- ====================================================
CREATE TABLE practice_errors (
    error_id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    practice_id INT NOT NULL COMMENT '對應原始的 practice_id (exercise_id)',
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    question_number INT COMMENT '題目編號',
    question_text TEXT COMMENT '題目內容',
    question_description TEXT COMMENT '題目說明',
    question_options JSON COMMENT '題目選項 (JSON格式)',
    user_option_code CHAR(1),
    user_option_text TEXT,
    correct_option_code CHAR(1),
    correct_option_text TEXT,
    explanation TEXT COMMENT '詳細解釋',
    error_type ENUM('concept_misunderstanding', 'calculation_error', 'careless_mistake', 'time_pressure') DEFAULT 'concept_misunderstanding',
    knowledge_point VARCHAR(100) COMMENT '相關知識點',
    difficulty_rating ENUM('easy', 'medium', 'hard'),
    review_status ENUM('not_reviewed', 'reviewed', 'mastered') DEFAULT 'not_reviewed',
    review_count INT DEFAULT 0,
    last_reviewed_at DATETIME,
    answer_duration INT DEFAULT 0 COMMENT '單題作答時間(秒)',
    answered_at DATETIME COMMENT '答題時間',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES practice_sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    INDEX idx_user_errors (user_id, review_status),
    INDEX idx_session_errors (session_id),
    INDEX idx_practice_errors (practice_id, user_id),
    INDEX idx_knowledge_point (knowledge_point)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 10. 學習統計表 (每日/每週/每月統計)
-- ====================================================
CREATE TABLE learning_statistics (
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    stat_date DATE NOT NULL,
    stat_type ENUM('daily', 'weekly', 'monthly') NOT NULL,
    courses_completed INT DEFAULT 0,
    practices_completed INT DEFAULT 0,
    questions_answered INT DEFAULT 0,
    correct_answers INT DEFAULT 0,
    study_duration_minutes INT DEFAULT 0,
    accuracy_rate DECIMAL(5,2) DEFAULT 0,
    streak_days INT DEFAULT 0 COMMENT '連續學習天數',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_stat (user_id, stat_date, stat_type),
    INDEX idx_user_stats (user_id, stat_type, stat_date),
    INDEX idx_stat_date (stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 11. 用戶學習偏好表
-- ====================================================
CREATE TABLE user_preferences (
    preference_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    preferred_difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    daily_study_goal_minutes INT DEFAULT 30,
    reminder_time TIME,
    timezone VARCHAR(50) DEFAULT 'Asia/Taipei',
    language ENUM('zh-TW', 'zh-CN', 'en') DEFAULT 'zh-TW',
    theme ENUM('light', 'dark', 'auto') DEFAULT 'light',
    notification_settings JSON COMMENT '通知設定',
    study_preferences JSON COMMENT '學習偏好設定',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_preference (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 12. 學習建議表
-- ====================================================
CREATE TABLE learning_suggestions (
    suggestion_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    course_id INT,
    suggestion_type ENUM('weak_area', 'review_needed', 'next_course', 'study_habit') NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    is_read BOOLEAN DEFAULT FALSE,
    is_dismissed BOOLEAN DEFAULT FALSE,
    action_taken BOOLEAN DEFAULT FALSE,
    valid_until DATE,
    metadata JSON COMMENT '建議相關的額外資料',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL,
    INDEX idx_user_suggestions (user_id, is_read),
    INDEX idx_suggestion_type (suggestion_type),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 13. 系統日誌表
-- ====================================================
CREATE TABLE system_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_user_logs (user_id, created_at),
    INDEX idx_action_type (action_type),
    INDEX idx_log_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- 創建視圖：用戶學習概覽
-- ====================================================
CREATE VIEW user_learning_overview AS
SELECT 
    u.user_id,
    u.username,
    u.real_name,
    COUNT(DISTINCT ucp.course_id) as completed_courses,
    COUNT(DISTINCT ps.session_id) as total_practices,
    AVG(ps.accuracy_rate) as avg_accuracy,
    MAX(ps.completed_at) as last_practice_date,
    SUM(ps.duration_seconds) as total_study_seconds
FROM users u
LEFT JOIN user_course_progress ucp ON u.user_id = ucp.user_id AND ucp.status = 'completed'
LEFT JOIN practice_sessions ps ON u.user_id = ps.user_id AND ps.is_completed = TRUE
GROUP BY u.user_id, u.username, u.real_name;

-- ====================================================
-- 創建視圖：課程統計
-- ====================================================
CREATE VIEW course_statistics AS
SELECT 
    c.course_id,
    c.title,
    c.category,
    COUNT(DISTINCT ucp.user_id) as enrolled_users,
    COUNT(DISTINCT CASE WHEN ucp.status = 'completed' THEN ucp.user_id END) as completed_users,
    COUNT(DISTINCT ps.session_id) as total_practices,
    AVG(ps.accuracy_rate) as avg_accuracy,
    COUNT(DISTINCT pe.error_id) as total_errors
FROM courses c
LEFT JOIN user_course_progress ucp ON c.course_id = ucp.course_id
LEFT JOIN practice_sessions ps ON c.course_id = ps.course_id AND ps.is_completed = TRUE
LEFT JOIN practice_errors pe ON ps.session_id = pe.session_id
GROUP BY c.course_id, c.title, c.category;

-- ====================================================
-- 創建觸發器：自動更新學習統計
-- ====================================================
DELIMITER //

CREATE TRIGGER update_daily_stats_after_practice
AFTER UPDATE ON practice_sessions
FOR EACH ROW
BEGIN
    IF NEW.is_completed = TRUE AND OLD.is_completed = FALSE THEN
        INSERT INTO learning_statistics (
            user_id, stat_date, stat_type, practices_completed, 
            questions_answered, correct_answers, study_duration_minutes, accuracy_rate
        ) VALUES (
            NEW.user_id, DATE(NEW.completed_at), 'daily',
            1, NEW.total_questions, NEW.correct_answers, 
            ROUND(NEW.duration_seconds / 60), NEW.accuracy_rate
        ) ON DUPLICATE KEY UPDATE
            practices_completed = practices_completed + 1,
            questions_answered = questions_answered + NEW.total_questions,
            correct_answers = correct_answers + NEW.correct_answers,
            study_duration_minutes = study_duration_minutes + ROUND(NEW.duration_seconds / 60),
            accuracy_rate = ROUND((correct_answers * 100.0) / questions_answered, 2),
            updated_at = CURRENT_TIMESTAMP;
    END IF;
END//

DELIMITER ;

-- ====================================================
-- 創建效能優化索引
-- ====================================================
CREATE INDEX idx_practice_completion ON practice_sessions(user_id, course_id, completed_at);
CREATE INDEX idx_user_answer_stats ON user_answers(user_id, question_id, is_correct);
CREATE INDEX idx_error_analysis ON practice_errors(user_id, knowledge_point, review_status);
CREATE INDEX idx_course_progress_status ON user_course_progress(status, completed_at);
CREATE INDEX idx_session_accuracy ON practice_sessions(course_id, accuracy_rate);

-- ====================================================
-- 完成訊息
-- ====================================================
SELECT 'Database schema created successfully!' as message;
SELECT CONCAT('Total tables created: ', COUNT(*)) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'goodin_learning_platform';
