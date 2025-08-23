from flask import Blueprint, request, jsonify
import mysql.connector

trade_history_bp = Blueprint('trade_history', __name__)

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # 修改為你的密碼
        database='goodin'
    )

@trade_history_bp.route('/api/trade_history', methods=['GET'])
def get_trade_history():
    account_id = request.args.get('account_id')
    sim_date = request.args.get('sim_date')  # 格式為 YYYY-MM-DD，僅歷史模擬用

    if not account_id:
        return jsonify({'error': '缺少 account_id'}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # 取得帳號類型
    cursor.execute("SELECT account_type FROM simulated_accounts WHERE account_id = %s", (account_id,))
    account_type_result = cursor.fetchone()
    if not account_type_result:
        return jsonify({'error': '找不到該 account_id'}), 404

    account_type = account_type_result['account_type']

    # 根據類型選擇不同查詢邏輯
    if account_type == 'historical':
        if not sim_date:
            return jsonify({'error': '歷史模擬帳戶需提供 sim_date'}), 400
        query = """
            SELECT 
                s.symbol,
                s.name,
                o.order_unit_type,
                o.order_type,
                o.deal_price,
                o.deal_quantity,
                o.transaction_fee,
                o.tax,
                o.order_time
            FROM orders o
            JOIN stocks s ON o.stock_id = s.stock_id
            WHERE o.account_id = %s
                AND DATE(o.order_time) = %s
                AND o.order_status IN ('已成交', '部分成交')
                AND o.deal_quantity > 0
            ORDER BY o.order_time DESC
        """
        cursor.execute(query, (account_id, sim_date))
    else:
        query = """
            SELECT 
                s.symbol,
                s.name,
                o.order_unit_type,
                o.order_type,
                o.deal_price,
                o.deal_quantity,
                o.transaction_fee,
                o.tax,
                o.order_time
            FROM orders o
            JOIN stocks s ON o.stock_id = s.stock_id
            WHERE o.account_id = %s
                AND o.order_status IN ('已成交', '部分成交')
                AND o.deal_quantity > 0
            ORDER BY o.order_time DESC
        """
        cursor.execute(query, (account_id,))

    rows = cursor.fetchall()

    for row in rows:
        total_amount = row['deal_price'] * row['deal_quantity']
        row['total_amount'] = round(total_amount - row['transaction_fee'] - row['tax'], 2)

    cursor.close()
    db.close()
    return jsonify(rows)
