# 📚 GOODIN 課程遷移與管理指南

> **更新日期**: 2025年8月20日  
> **狀態**: 已完成 Course 1-9 支援  
> **工具版本**: Universal Course Migrator v2.0

## 🎯 概述

本指南介紹如何使用**通用課程遷移工具**將 GOODIN 學習平台的課程內容從 API 檔案遷移到 MySQL 資料庫中。

## 📋 支援的課程清單

| 課程編號 | 課程名稱 | 頁面數量 | 特殊功能 | 狀態 |
|---------|----------|---------|---------|------|
| Course 1 | 技術分析入門 | 9 頁 | 多步驟、圖表 | ✅ 已支援 |
| Course 2 | 基本面分析 | 19 頁 | 多步驟、表格 | ✅ 已支援 |
| Course 3 | K線圖基礎 | 10 頁 | 圖表、輪播 | ✅ 已支援 |
| Course 4 | 簡單移動平均線 | 8 頁 | 多圖表 | ✅ 已支援 |
| Course 5 | 相對強弱指標 RSI | 9 頁 | 數學公式、圖表 | ✅ 已支援 |
| Course 6 | 布林通道 | - | 波動率指標 | ✅ 已支援 |
| Course 7 | MACD指標進階 | - | 進階技術分析 | ✅ 已支援 |
| Course 8 | KD隨機指標 | 11 頁 | 多圖表、多步驟 | ✅ 已支援 |
| Course 9 | 乖離率 BIAS | 13 頁 | 輪播、數學公式 | ✅ 已支援 |

## 🚀 快速開始

### 1. 環境準備

```bash
# 確保 MySQL 服務運行
sudo systemctl start mysql

# 進入專案目錄
cd /home/crab79/repo/115_project_venv/backend

# 啟動虛擬環境（如果需要）
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 2. 建立資料庫

```bash
# 使用乾淨的資料庫架構
mysql -u root -p < database_schema_clean.sql
```

### 3. 遷移課程資料

```bash
# 遷移單一課程（例如課程1）
python3 universal_course_migrator.py 1

# 遷移多個課程
python3 universal_course_migrator.py 1
python3 universal_course_migrator.py 2
python3 universal_course_migrator.py 3
# ... 以此類推
```

## 🔧 通用遷移工具功能

### 支援的課程功能
- ✅ **基本頁面內容**: HTML 內容處理
- ✅ **圖表功能**: chart1, chart2, chart3 等
- ✅ **多步驟顯示**: progressive content reveal
- ✅ **輪播圖片**: carousel_items 支援
- ✅ **數學公式**: LaTeX 格式保留
- ✅ **互動元素**: 按鈕、iframe 等

### 自動處理功能
- 🔄 **動態載入**: 自動發現並載入課程 API 檔案
- 🛡️ **資料驗證**: 檢查資料完整性
- 🗄️ **重複處理**: 智能處理重複資料
- 📊 **進度顯示**: 詳細的遷移進度報告

## 📁 專案結構

```
backend/
├── 📋 COURSE_MIGRATION_GUIDE.md    # 本檔案
├── 📋 DATABASE_SETUP_GUIDE.md      # 資料庫設定指南
├── 📋 README.md                    # 專案說明
│
├── 🔧 universal_course_migrator.py # 🌟 核心遷移工具
├── 🗄️ database_schema_clean.sql   # 🌟 乾淨資料庫架構
│
├── api/                            # 課程 API 檔案
│   ├── course1_api.py ~ course9_api.py
│   ├── progress_api.py
│   └── stock_api.py
│
├── 🐍 app.py                       # Flask 主應用
├── 📄 requirements.txt             # Python 依賴
└── utils/                          # 工具模組
```

## 🎨 課程功能詳解

### 標準功能
所有課程都支援以下標準功能：
- **頁面導航**: 上一頁/下一頁按鈕
- **內容顯示**: HTML 格式內容
- **響應式設計**: 適配不同螢幕大小

### 進階功能

#### 1. 圖表功能 (Chart Types)
```python
"chart_type": "chart1"  # 支援 chart1, chart2, chart3, chart4, chart5
```
- 用於股價圖表、技術指標顯示
- 支援互動操作

#### 2. 多步驟顯示 (Multi-steps)
```python
"multi_steps": ["text1", "text2", "carousel"]
```
- 漸進式內容揭示
- 提升學習體驗

#### 3. 圖片輪播 (Carousel)
```python
"carousel_items": [
    {
        "src": "image_url",
        "alt": "description", 
        "caption": "標題",
        "credit": "來源說明"
    }
]
```
- 支援多張圖片輪播
- 自動圖片來源標註

## 🔍 遷移後驗證

### 1. 資料庫檢查
```sql
-- 檢查課程資料
SELECT course_id, course_name, course_description FROM courses;

-- 檢查頁面數量
SELECT course_id, COUNT(*) as page_count 
FROM course_pages 
GROUP BY course_id;

-- 檢查特殊功能
SELECT course_id, COUNT(*) as chart_pages 
FROM course_pages 
WHERE chart_type IS NOT NULL 
GROUP BY course_id;
```

### 2. API 適配
遷移完成後，需要修改對應的 API 檔案從資料庫讀取資料：

```python
# 修改前 (硬編碼)
course1_pages = [...]

# 修改後 (資料庫讀取)
def get_course1_content():
    # 從資料庫讀取課程頁面
    pages = get_course_pages_from_db(course_id=1)
    return jsonify({"pages": pages})
```

## 🚨 故障排除

### 常見問題

#### 1. 資料庫連接失敗
```bash
❌ 資料庫連接失敗: Access denied for user 'root'@'localhost'
```
**解決方案**: 檢查 MySQL 用戶權限和密碼

#### 2. 課程檔案無法載入
```bash
❌ 無法載入課程5資料: No module named 'course5_api'
```
**解決方案**: 確保 `course5_api.py` 存在於 `api/` 目錄中

#### 3. JSON 序列化錯誤
```bash
❌ Object of type 'datetime' is not JSON serializable
```
**解決方案**: 檢查課程資料中是否包含無法序列化的物件

### 除錯模式
```bash
# 啟用詳細日誌
python3 universal_course_migrator.py 1 --verbose

# 僅驗證不執行
python3 universal_course_migrator.py 1 --dry-run
```

## 📈 效能最佳化

### 建議設定
- **批次大小**: 50 頁面/批次
- **連接池**: 5-10 連接
- **字符編碼**: UTF8MB4
- **索引**: 已優化課程和頁面查詢索引

## 🔒 安全考量

### 資料保護
- **外鍵約束**: 確保資料完整性
- **輸入驗證**: 防止 SQL 注入
- **備份機制**: 建議定期備份
- **權限控制**: 最小權限原則

## 📞 技術支援

### 檢查清單
- [ ] MySQL 5.7+ 或 MariaDB 10.2+
- [ ] Python 3.8+
- [ ] mysql-connector-python 包
- [ ] 足夠的資料庫權限
- [ ] UTF8MB4 字符集支援

### 聯絡資訊
如需技術支援，請提供：
1. 錯誤訊息完整內容
2. 課程編號和問題頁面
3. MySQL 版本資訊
4. Python 環境詳情

---

## 🎉 完成！

遷移完成後，您將擁有：
- 🗄️ 結構化的資料庫內容
- 🔄 可擴展的課程管理系統  
- 📊 詳細的學習分析功能
- 🛡️ 安全可靠的資料存儲

**下一步**: 修改前端 API 調用，從資料庫讀取課程內容並測試所有功能！
