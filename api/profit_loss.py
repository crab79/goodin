from flask import Blueprint, request, jsonify
import mysql.connector
from datetime import datetime
from utils.config import DB_CONFIG

profit_loss_bp = Blueprint('profit_loss', __name__)

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


@profit_loss_bp.route('/api/profit_loss', methods=['GET'])
def calculate_profit_loss():
    account_id = request.args.get('account_id')
    simulation_date = request.args.get('simulation_date')  # 僅歷史模擬需傳入

    if not account_id:
        return jsonify({'error': '缺少 account_id'}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # 確認帳戶類型
    cursor.execute("SELECT account_type FROM simulated_accounts WHERE account_id = %s", (account_id,))
    account_row = cursor.fetchone()
    if not account_row:
        return jsonify({'error': '帳戶不存在'}), 404

    account_type = account_row['account_type']

    # 查詢持股
    cursor.execute("""
        SELECT h.stock_id, h.quantity, h.purchase_price, s.symbol, s.name
        FROM holdings h
        JOIN stocks s ON h.stock_id = s.stock_id
        WHERE h.account_id = %s
    """, (account_id,))
    holdings = cursor.fetchall()

    unrealized_total = 0
    for holding in holdings:
        stock_id = holding['stock_id']
        quantity = holding['quantity']
        purchase_price = holding['purchase_price']

        # 根據帳戶類型查即時或歷史價格
        if account_type == 'realtime':
            cursor.execute("""
                SELECT price FROM raw_stock_data
                WHERE stock_id = %s ORDER BY time DESC LIMIT 1
            """, (stock_id,))
        elif account_type == 'history':
            if not simulation_date:
                return jsonify({'error': '歷史模擬帳戶必須提供 simulation_date'}), 400
            cursor.execute("""
                SELECT close FROM kline_data
                WHERE stock_id = %s AND interval_type = '1d' AND DATE(time) = %s
                ORDER BY time DESC LIMIT 1
            """, (stock_id, simulation_date))
        else:
            continue

        price_row = cursor.fetchone()
        if not price_row:
            continue

        current_price = price_row.get('price') or price_row.get('close')
        unrealized_profit = (current_price - purchase_price) * quantity
        holding['current_price'] = float(current_price)
        holding['unrealized_profit'] = round(unrealized_profit, 2)
        unrealized_total += unrealized_profit

    # 計算已實現損益
    cursor.execute("""
        SELECT stock_id, order_type, quantity, deal_price FROM transactions
        WHERE account_id = %s
    """, (account_id,))
    transactions = cursor.fetchall()

    realized_total = 0
    total_cost = {}

    for tx in transactions:
        stock_id = tx['stock_id']
        qty = tx['quantity']
        price = tx['deal_price']
        if tx['order_type'] == 'buy':
            total_cost.setdefault(stock_id, []).append((qty, price))
        elif tx['order_type'] == 'sell':
            buy_list = total_cost.get(stock_id, [])
            sold = qty
            while sold > 0 and buy_list:
                buy_qty, buy_price = buy_list[0]
                match_qty = min(sold, buy_qty)
                realized_total += (price - buy_price) * match_qty
                sold -= match_qty
                if match_qty == buy_qty:
                    buy_list.pop(0)
                else:
                    buy_list[0] = (buy_qty - match_qty, buy_price)

    db.close()

    return jsonify({
        'account_type': account_type,
        'realized_profit': round(realized_total, 2),
        'unrealized_profit': round(unrealized_total, 2),
        'holdings': holdings
    })
