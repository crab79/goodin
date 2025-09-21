from flask import Blueprint, request, jsonify
import mysql.connector
from datetime import datetime
from utils.config import DB_CONFIG

trade_history_bp = Blueprint('trade_history', __name__)

# 歷史模擬股市：僅輸出下單紀錄
@trade_history_bp.route('/history', methods=['GET'])
def get_historical_trade_history():
    account_id = request.args.get('account_id')
    trade_date = request.args.get('trade_date')  # 格式：YYYY-MM-DD

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                s.symbol AS 股票代碼,
                s.name AS 股票名稱,
                o.order_unit_type AS 整股零股,
                CASE o.order_type
                    WHEN 'buy_limit' THEN CONCAT('買入（限價 ', o.order_price, ' 元）')
                    WHEN 'buy_market' THEN '買入（市價）'
                    WHEN 'sell_limit' THEN CONCAT('賣出（限價 ', o.order_price, ' 元）')
                    WHEN 'sell_market' THEN '賣出（市價）'
                END AS 交易類型,
                DATE(o.order_time) AS 下單日期,
                CASE o.order_status
                    WHEN '已成交' THEN '成交'
                    ELSE '未成交'
                END AS 是否成交
            FROM orders o
            JOIN stocks s ON o.stock_id = s.stock_id
            WHERE o.account_id = %s AND DATE(o.order_time) = %s
            ORDER BY o.order_time DESC
        """
        cursor.execute(query, (account_id, trade_date))
        results = cursor.fetchall()
        return jsonify(results)

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# 即時模擬股市：輸出完整成交明細
@trade_history_bp.route('/realtime', methods=['GET'])
def get_realtime_trade_history():
    account_id = request.args.get('account_id')
    trade_date = request.args.get('trade_date')  # 格式：YYYY-MM-DD

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                s.symbol AS 股票代碼,
                s.name AS 股票名稱,
                o.order_unit_type AS 整股零股,
                CASE o.order_type
                    WHEN 'buy_limit' THEN '買入'
                    WHEN 'buy_market' THEN '買入'
                    WHEN 'sell_limit' THEN '賣出'
                    WHEN 'sell_market' THEN '賣出'
                END AS 交易類型,
                t.deal_price AS 成交價,
                t.quantity AS 張數,
                t.deal_time AS 時間
            FROM transactions t
            JOIN orders o ON t.order_id = o.order_id
            JOIN stocks s ON o.stock_id = s.stock_id
            WHERE o.account_id = %s AND DATE(t.deal_time) = %s
            ORDER BY t.deal_time DESC
        """
        cursor.execute(query, (account_id, trade_date))
        results = cursor.fetchall()
        return jsonify(results)

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
