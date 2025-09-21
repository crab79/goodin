from flask import Blueprint, jsonify, request
import mysql.connector
from datetime import datetime, date
from utils.config import DB_CONFIG

order_bp = Blueprint('orders', __name__)

def get_db():
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


# 查詢訂單（分成今日與歷史）
@order_bp.route('/api/orders', methods=['GET'])
def get_orders():
    from flask import session
    account_id = request.args.get('account_id') or session.get('selected_account_id')
    if not account_id:
        return jsonify({'ok': False, 'error': '缺少 account_id'}), 400
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            o.order_id,
            s.symbol AS stock_symbol,
            s.name AS stock_name,
            o.order_type,
            o.order_unit_type,
            o.order_status,
            o.order_method,
            o.quantity,
            o.order_price,
            o.deal_quantity,
            o.deal_price,
            o.order_time
        FROM orders o
        JOIN stocks s ON o.stock_id = s.stock_id
        WHERE o.account_id = %s
        ORDER BY o.order_time DESC
    """
    cursor.execute(query, (account_id,))
    results = cursor.fetchall()

    today = date.today()
    today_orders = []
    history_orders = []

    for row in results:
        row["order_time"] = row["order_time"].strftime("%Y-%m-%d %H:%M")
        undeal_quantity = row["quantity"] - (row["deal_quantity"] or 0)
        undeal_amount = undeal_quantity * float(row["order_price"])
        row["undeal_quantity"] = undeal_quantity
        row["undeal_amount"] = undeal_amount

        # 今日 or 歷史分類
        order_date = datetime.strptime(row["order_time"], "%Y-%m-%d %H:%M").date()
        if order_date == today:
            today_orders.append(row)
        else:
            history_orders.append(row)

    cursor.close()
    db.close()

    return jsonify({
        "today_orders": today_orders,
        "history_orders": history_orders
    })


# 刪除指定委託單（設為「已取消」）
@order_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    db = get_db()
    cursor = db.cursor()

    query = "UPDATE orders SET order_status = '已取消' WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    db.commit()

    success = cursor.rowcount > 0

    cursor.close()
    db.close()

    if success:
        return jsonify({'ok': True, 'message': '委託單已取消'})
    else:
        return jsonify({'ok': False, 'error': '找不到此筆委託單'}), 404
