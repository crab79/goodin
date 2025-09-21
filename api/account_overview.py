from flask import Blueprint, request, jsonify
import mysql.connector
from datetime import datetime, timedelta
from utils.config import DB_CONFIG
account_overview_bp = Blueprint('account_overview', __name__)


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


#  計算今日損益率：今日總市值 - 昨日總市值 / 昨日總市值
def calculate_daily_profit_rate(today_value, yesterday_value):
    if yesterday_value == 0:
        return 0
    return round(((today_value - yesterday_value) / yesterday_value) * 100, 2)

#  即時模擬帳戶總覽
@account_overview_bp.route('/api/account_overview/realtime', methods=['GET'])
def realtime_account_overview():
    account_id = request.args.get('account_id')
    if not account_id:
        return jsonify({'error': '缺少 account_id'}), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 1. 取得帳戶現金與類型
    cursor.execute("""
        SELECT account_type, cash AS cash_balance
        FROM simulated_accounts
        WHERE account_id = %s AND account_type = 'realtime'
    """, (account_id,))
    account = cursor.fetchone()
    if not account:
        return jsonify({'error': '找不到帳戶'}), 404

    cash_balance = account['cash_balance']
    account_type = account['account_type']

    # 2. 查詢持股與即時市價
    cursor.execute("""
        SELECT 
            s.symbol,
            s.name,
            h.quantity,
            h.purchase_price AS avg_cost,
            rs.price AS market_price,
            rs.time AS price_time,
            s.stock_id
        FROM holdings h
        JOIN stocks s ON h.stock_id = s.stock_id
        LEFT JOIN raw_stock_data rs ON s.last_price_id = rs.id
        WHERE h.account_id = %s
    """, (account_id,))
    holdings = cursor.fetchall()

    total_market_value = 0
    total_cost_value = 0
    total_yesterday_value = 0
    holdings_detail = []

    for row in holdings:
        stock_id = row["stock_id"]
        quantity = row["quantity"]
        avg_cost = row["avg_cost"]
        market_price = row["market_price"]

        # 成本與市值計算
        cost_value = quantity * avg_cost
        market_value = quantity * market_price
        profit = market_value - cost_value
        profit_rate = round((profit / cost_value) * 100, 2) if cost_value else 0

        total_cost_value += cost_value
        total_market_value += market_value

        # 昨日收盤價抓取（使用 raw_stock_data 往前一天找最近的收盤）
        cursor.execute("""
            SELECT price FROM raw_stock_data 
            WHERE stock_id = %s AND time < CURDATE()
            ORDER BY time DESC LIMIT 1
        """, (stock_id,))
        yesterday = cursor.fetchone()
        yesterday_price = yesterday['price'] if yesterday else market_price
        total_yesterday_value += yesterday_price * quantity

        holdings_detail.append({
            "symbol": row["symbol"],
            "name": row["name"],
            "quantity": quantity,
            "avg_cost": round(avg_cost, 2),
            "market_price": round(market_price, 2),
            "market_value": round(market_value, 2),
            "profit": round(profit, 2),
            "profit_rate": f"{profit_rate}%"
        })

    total_assets = cash_balance + total_market_value
    total_profit_loss_rate = round(((total_assets - (cash_balance + total_cost_value)) / (cash_balance + total_cost_value)) * 100, 2) if (cash_balance + total_cost_value) else 0
    today_profit_loss_rate = calculate_daily_profit_rate(total_market_value, total_yesterday_value)

    cursor.close()
    db.close()

    return jsonify({
        "account_id": int(account_id),
        "account_type": account_type,
        "cash_balance": round(cash_balance, 2),
        "market_value": round(total_market_value, 2),
        "total_assets": round(total_assets, 2),
        "total_profit_loss_rate": f"{total_profit_loss_rate}%",
        "today_profit_loss_rate": f"{today_profit_loss_rate}%",
        "holdings": holdings_detail
    })

#  歷史模擬帳戶總覽
@account_overview_bp.route('/api/account_overview/history', methods=['GET'])
def history_account_overview():
    account_id = request.args.get('account_id')
    date_str = request.args.get('date')  # 可為 None
    if not account_id:
        return jsonify({'error': '缺少 account_id'}), 400

    sim_date = None
    if date_str:
        try:
            try:
                sim_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                sim_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT").date()
        except ValueError:
            return jsonify({'error': '日期格式錯誤，請使用 YYYY-MM-DD 或 RFC 1123'}), 400

    print(f"[DEBUG] account_id: {account_id}, sim_date: {sim_date}")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 1. 取得帳戶現金與類型
    cursor.execute("""
        SELECT account_type, cash AS cash_balance
        FROM simulated_accounts
        WHERE account_id = %s AND account_type = 'history'
    """, (account_id,))
    account = cursor.fetchone()
    if not account:
        return jsonify({'error': '找不到歷史帳戶'}), 404

    cash_balance = account['cash_balance']
    account_type = account['account_type']

    # 2. 查詢持股與該日或最新一日 K 線收盤價
    if sim_date:
        # 查詢每檔持股 sim_date 之後最近一天的 K 線收盤價
        cursor.execute("""
            SELECT 
                s.symbol,
                s.name,
                h.quantity,
                h.purchase_price AS avg_cost,
                k.close AS market_price,
                s.stock_id
            FROM holdings h
            JOIN stocks s ON h.stock_id = s.stock_id
            JOIN (
                SELECT k1.stock_id, MIN(k1.time) AS min_time
                FROM kline_data k1
                WHERE k1.time >= %s AND k1.interval_type = '1d'
                GROUP BY k1.stock_id
            ) next_k ON h.stock_id = next_k.stock_id
            JOIN kline_data k ON h.stock_id = k.stock_id AND k.time = next_k.min_time AND k.interval_type = '1d'
            WHERE h.account_id = %s
        """, (sim_date, account_id))
    else:
        # 查詢每檔持股的最新一日收盤價
        cursor.execute("""
            SELECT 
                s.symbol,
                s.name,
                h.quantity,
                h.purchase_price AS avg_cost,
                k.close AS market_price,
                s.stock_id
            FROM holdings h
            JOIN stocks s ON h.stock_id = s.stock_id
            JOIN (
                SELECT stock_id, MAX(time) AS max_time
                FROM kline_data
                WHERE interval_type = '1d'
                GROUP BY stock_id
            ) latest ON h.stock_id = latest.stock_id
            JOIN kline_data k ON h.stock_id = k.stock_id AND k.time = latest.max_time AND k.interval_type = '1d'
            WHERE h.account_id = %s
        """, (account_id,))
    holdings = cursor.fetchall()
    print(f"[DEBUG] holdings: {holdings}")

    total_market_value = 0
    total_cost_value = 0
    holdings_detail = []

    for row in holdings:
        quantity = row["quantity"]
        avg_cost = row["avg_cost"]
        market_price = row["market_price"]

        cost_value = quantity * avg_cost
        market_value = quantity * market_price
        profit = market_value - cost_value
        profit_rate = round((profit / cost_value) * 100, 2) if cost_value else 0

        total_cost_value += cost_value
        total_market_value += market_value

        holdings_detail.append({
            "symbol": row["symbol"],
            "name": row["name"],
            "quantity": quantity,
            "avg_cost": round(avg_cost, 2),
            "market_price": round(market_price, 2),
            "market_value": round(market_value, 2),
            "profit": round(profit, 2),
            "profit_rate": f"{profit_rate}%"
        })

    total_assets = cash_balance + total_market_value
    total_profit_loss_rate = round(((total_assets - (cash_balance + total_cost_value)) / (cash_balance + total_cost_value)) * 100, 2) if (cash_balance + total_cost_value) else 0

    cursor.close()
    db.close()

    return jsonify({
        "account_id": int(account_id),
        "account_type": account_type,
        "cash_balance": round(cash_balance, 2),
        "market_value": round(total_market_value, 2),
        "total_assets": round(total_assets, 2),
        "total_profit_loss_rate": f"{total_profit_loss_rate}%",
        "today_profit_loss_rate": "N/A",  # 歷史資料無法提供每日變化
        "holdings": holdings_detail
    })
