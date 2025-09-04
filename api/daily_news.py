"""
每日新聞 API
從遠端資料庫抓取每日新聞資料傳送到前端
"""

from flask import Blueprint, jsonify
import mysql.connector
from datetime import datetime
import traceback
import sys
import os

# 添加 backend 路徑到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from utils.config import DB_CONFIG

daily_news_api = Blueprint('daily_news_api', __name__)

def get_db_connection():
    """建立資料庫連接"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset='utf8mb4',
            autocommit=True
        )
        return connection
    except mysql.connector.Error as err:
        print(f"資料庫連接錯誤: {err}")
        return None

@daily_news_api.route('/api/daily_news', methods=['GET'])
def get_daily_news():
    """
    獲取每日新聞資料
    返回格式符合前端期望的結構
    """
    try:
        # 建立資料庫連接
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'status': 'error',
                'message': '資料庫連接失敗'
            }), 500

        cursor = connection.cursor(dictionary=True)
        
        # 查詢今日新聞（按日期降序排列，最新的在前面）
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
        SELECT id, 日期 as date, 來源 as source, 標題 as title, 連結 as link 
        FROM daily_news 
        WHERE DATE(日期) = %s 
        ORDER BY 日期 DESC 
        LIMIT 20
        """
        
        cursor.execute(query, (today,))
        news_data = cursor.fetchall()
        
        # 如果今天沒有新聞，則取最近的新聞
        if not news_data:
            query = """
            SELECT id, 日期 as date, 來源 as source, 標題 as title, 連結 as link 
            FROM daily_news 
            ORDER BY 日期 DESC 
            LIMIT 20
            """
            cursor.execute(query)
            news_data = cursor.fetchall()
        
        # 關閉連接
        cursor.close()
        connection.close()
        
        # 處理返回資料格式
        formatted_news = []
        for news in news_data:
            formatted_news.append({
                'id': news['id'],
                'title': news['title'],
                'link': news['link'],
                'source': news['source'],
                'date': news['date'].strftime('%Y-%m-%d %H:%M:%S') if news['date'] else None
            })
        
        return jsonify({
            'status': 'success',
            'message': f'成功獲取 {len(formatted_news)} 則新聞',
            'data': formatted_news,
            'count': len(formatted_news)
        })
        
    except mysql.connector.Error as db_err:
        error_msg = f"資料庫錯誤: {str(db_err)}"
        print(error_msg)
        return jsonify({
            'status': 'error',
            'message': error_msg
        }), 500
        
    except Exception as e:
        error_msg = f"伺服器錯誤: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': error_msg
        }), 500

@daily_news_api.route('/api/daily_news/latest', methods=['GET'])
def get_latest_news():
    """
    獲取最新新聞資料（不限定今天）
    """
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'status': 'error',
                'message': '資料庫連接失敗'
            }), 500

        cursor = connection.cursor(dictionary=True)
        
        # 查詢最新的新聞（前20則）
        query = """
        SELECT id, 日期 as date, 來源 as source, 標題 as title, 連結 as link 
        FROM daily_news 
        ORDER BY 日期 DESC 
        LIMIT 20
        """
        
        cursor.execute(query)
        news_data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        # 處理返回資料格式
        formatted_news = []
        for news in news_data:
            formatted_news.append({
                'id': news['id'],
                'title': news['title'],
                'link': news['link'],
                'source': news['source'],
                'date': news['date'].strftime('%Y-%m-%d %H:%M:%S') if news['date'] else None
            })
        
        return jsonify({
            'status': 'success',
            'message': f'成功獲取 {len(formatted_news)} 則最新新聞',
            'data': formatted_news,
            'count': len(formatted_news)
        })
        
    except Exception as e:
        error_msg = f"伺服器錯誤: {str(e)}"
        print(error_msg)
        return jsonify({
            'status': 'error',
            'message': error_msg
        }), 500

@daily_news_api.route('/api/daily_news/test', methods=['GET'])
def test_daily_news_connection():
    """
    測試資料庫連接和資料表結構
    """
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'status': 'error',
                'message': '資料庫連接失敗'
            }), 500

        cursor = connection.cursor(dictionary=True)
        
        # 測試資料表是否存在並獲取結構
        cursor.execute("DESCRIBE daily_news")
        table_structure = cursor.fetchall()
        
        # 獲取資料表中的資料數量
        cursor.execute("SELECT COUNT(*) as count FROM daily_news")
        count_result = cursor.fetchone()
        total_count = count_result['count']
        
        # 獲取最新的一筆資料作為範例
        cursor.execute("SELECT * FROM daily_news ORDER BY 日期 DESC LIMIT 1")
        sample_data = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'status': 'success',
            'message': '資料庫連接成功',
            'table_structure': table_structure,
            'total_records': total_count,
            'sample_data': sample_data
        })
        
    except Exception as e:
        error_msg = f"測試失敗: {str(e)}"
        print(error_msg)
        return jsonify({
            'status': 'error',
            'message': error_msg
        }), 500
