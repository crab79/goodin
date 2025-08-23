from flask import Blueprint, request, jsonify
import mysql.connector

account_overview_bp = Blueprint('account_overview', __name__)

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # ← 修改為你自己的密碼
        database='goodin'
    )

# 即時股市帳號總覽
@account_overview_bp.route('/api/account_overview/realtime', methods=['GET'])
def realtime_account_overview():
    account_id = request.args.get('account_id')
    if not account_id:
        return jsonify({'error': '缺少 account_id'}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT 
            s.symbol,
            s.name,
            h.quantity,
            h.avg_cost,
            s.last_price AS market_price
        FROM holdings h
        JOIN stocks s ON h.stock_id = s.stock_id
        JOIN simulated_accounts a ON h.account_id = a.account_id
        WHERE h.account_id = %s AND a.account_type = 'realtime'
    """
    cursor.execute(query, (account_id,))
    results = cursor.fetchall()

    for row in results:
        market_value = row["market_price"] * row["quantity"]
        cost_value = row["avg_cost"] * row["quantity"]
        profit = market_value - cost_value
        profit_rate = round((profit / cost_value) * 100, 2) if cost_value else 0

        row["market_value"] = round(market_value, 2)
        row["profit"] = round(profit, 2)
        row["profit_rate"] = f"{profit_rate}%"

    cursor.close()
    db.close()
    return jsonify(results)


# 歷史股市帳號總覽
@account_overview_bp.route('/api/account_overview/history', methods=['GET'])
def history_account_overview():
    account_id = request.args.get('account_id')
    date = request.args.get('date')  # YYYY-MM-DD

    if not account_id or not date:
        return jsonify({'error': '缺少 account_id 或 date'}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT 
            s.symbol,
            s.name,
            h.quantity,
            h.avg_cost,
            k.close AS market_price
        FROM holdings h
        JOIN stocks s ON h.stock_id = s.stock_id
        JOIN k_line k ON h.stock_id = k.stock_id
        JOIN simulated_accounts a ON h.account_id = a.account_id
        WHERE h.account_id = %s 
            AND a.account_type = 'historical'
            AND k.date = %s
    """
    cursor.execute(query, (account_id, date))
    results = cursor.fetchall()

    for row in results:
        market_value = row["market_price"] * row["quantity"]
        cost_value = row["avg_cost"] * row["quantity"]
        profit = market_value - cost_value
        profit_rate = round((profit / cost_value) * 100, 2) if cost_value else 0

        row["market_value"] = round(market_value, 2)
        row["profit"] = round(profit, 2)
        row["profit_rate"] = f"{profit_rate}%"

    cursor.close()
    db.close()
    return jsonify(results)
