# 資料庫建立與遷移指南

## 📋 檔案說明

我已經為您創建了以下 SQL 檔案，可以直接複製貼上到您的 MySQL 主機執行：

### 1. `create_database.sql` - 主要資料庫建立腳本
- **功能**: 建立完整的資料庫架構
- **包含**: 12個資料表、索引、觸發器、視圖
- **使用方式**: 直接複製整個檔案內容到 MySQL 執行

### 2. `migrate_data.sql` - 資料遷移腳本
- **功能**: 將您現有的假資料轉移到真實資料庫
- **包含**: 對應 `progress_api.py` 中所有假資料的插入語句
- **使用方式**: 在建立資料庫後執行此腳本

## 🚀 快速部署步驟

### 步驟 1: 建立資料庫架構
```sql
-- 複製 create_database.sql 的完整內容並執行
-- 或者使用指令導入
mysql -u root -p < create_database.sql
```

### 步驟 2: 遷移現有資料
```sql
-- 複製 migrate_data.sql 的完整內容並執行
-- 或者使用指令導入
mysql -u root -p goodin_learning_platform < migrate_data.sql
```

### 步驟 3: 驗證資料
```sql
USE goodin_learning_platform;

-- 檢查資料表
SHOW TABLES;

-- 檢查課程資料
SELECT * FROM courses;

-- 檢查用戶進度
SELECT * FROM user_course_progress;

-- 檢查練習記錄
SELECT * FROM practice_sessions;

-- 檢查錯題記錄
SELECT * FROM practice_errors;
```

## 📊 資料庫架構重點

### 核心資料表對應關係

| 原始假資料 | 對應資料表 | 說明 |
|------------|------------|------|
| `fake_courses` | `courses` | 課程基本資訊 |
| `fake_user_course_progress` | `user_course_progress` | 用戶課程完成進度 |
| `fake_user_practice_progress` | `practice_sessions` | 練習活動記錄 |
| `fake_practice_errors` | `practice_errors` | 錯題詳細記錄 |

### 新增的進階功能表

| 資料表名稱 | 功能說明 |
|------------|----------|
| `questions` | 題目庫管理 |
| `question_options` | 題目選項管理 |
| `user_answers` | 詳細答題記錄 |
| `learning_statistics` | 學習統計分析 |
| `learning_suggestions` | 智能學習建議 |
| `user_preferences` | 用戶偏好設定 |
| `system_logs` | 系統操作日誌 |

## 🔧 API 適配說明

您的 `progress_api.py` 需要進行以下調整：

### 1. 資料庫連接設定
```python
import mysql.connector
from mysql.connector import Error

# 資料庫配置
DB_CONFIG = {
    'host': 'your_host',
    'database': 'goodin_learning_platform',
    'user': 'your_username',
    'password': 'your_password',
    'charset': 'utf8mb4'
}
```

### 2. 主要 API 端點對應

| API 端點 | 對應資料表查詢 |
|----------|----------------|
| `/api/complete_course` | `INSERT INTO user_course_progress` |
| `/api/complete_practice` | `INSERT INTO practice_sessions + practice_errors` |
| `/api/learning_analytics/<user_id>` | `SELECT FROM user_course_progress, practice_sessions` |
| `/api/practice_analysis/<user_id>` | `SELECT FROM practice_sessions, practice_errors` |
| `/api/learning_suggestions/<user_id>` | `SELECT FROM learning_suggestions` |

## 📈 優勢特色

### ✅ 完整相容性
- 100% 相容現有 API 結構
- 保持所有原始功能
- 無需修改前端程式碼

### ✅ 擴展性設計
- 支援多用戶系統
- 完整的學習分析功能
- 智能建議系統
- 詳細的錯題追蹤

### ✅ 效能最佳化
- 合理的索引設計
- 查詢效能優化
- 自動統計更新
- 資料關聯完整性

### ✅ 安全性考量
- 外鍵約束確保資料完整性
- 用戶權限分級管理
- 操作日誌追蹤
- 資料備份機制

## 🛠️ 故障排除

### 常見問題
1. **字符編碼問題**: 確保使用 `utf8mb4` 字符集
2. **外鍵約束錯誤**: 按照檔案順序執行 SQL 腳本
3. **權限不足**: 確保 MySQL 用戶有建立資料庫權限

### 檢查指令
```sql
-- 檢查字符集
SHOW CREATE DATABASE goodin_learning_platform;

-- 檢查外鍵約束
SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
WHERE REFERENCED_TABLE_SCHEMA = 'goodin_learning_platform';

-- 檢查資料完整性
SELECT 
    TABLE_NAME, 
    TABLE_ROWS 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'goodin_learning_platform';
```

## 📞 技術支援

如有任何問題，請檢查以下項目：
1. MySQL 版本是否為 5.7 或更高
2. 是否有足夠的資料庫權限
3. 字符編碼設定是否正確
4. 外鍵約束是否正常運作

---

**完成後，您就可以將假資料系統升級為完整的資料庫驅動系統！** 🎉
