from flask import Blueprint, request, jsonify, session
from datetime import datetime
from sqlalchemy import text
from utils.config import engine

holding_bp = Blueprint('holdings', __name__)

# 公用函式：計算損益與報酬率
def enrich_holding(row):
    estimated_profit = (row.current_price - row.avg_price) * row.total_quantity if row.current_price else 0
    return_rate = (estimated_profit / (row.avg_price * row.total_quantity) * 100) if row.avg_price else 0
    return {
        'stock_id': row.stock_id,
        'symbol': row.symbol,
        'name': row.name,
        'holding_type': row.holding_type,
        'available_quantity': row.available_quantity,
        'total_quantity': row.total_quantity,
        'avg_price': float(row.avg_price),
        'current_price': float(row.current_price) if row.current_price else None,
        'estimated_profit': round(estimated_profit),
        'return_rate': f"{return_rate:.2f}%" if row.current_price else None
    }

# 1. 歷史模擬庫存明細 API
@holding_bp.route('/api/holdings/history', methods=['GET'])
def get_historical_holdings():
    account_id = session.get('selected_account_id')
    date_str = request.args.get('date')  # 格式 YYYY-MM-DD

    if not account_id or not date_str:
        return jsonify({'ok': False, 'error': '缺少 account_id 或 date'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'ok': False, 'error': '日期格式錯誤'}), 400

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT h.stock_id, s.symbol, s.name, h.holding_type,
                   h.available_quantity, h.quantity AS total_quantity, h.purchase_price AS avg_price,
                   hp.price AS current_price
            FROM historical_holdings h
            JOIN stocks s ON h.stock_id = s.stock_id
            LEFT JOIN historical_prices hp
              ON h.stock_id = hp.stock_id AND hp.date = :date
            WHERE h.account_id = :account_id AND h.date = :date
        """), {'account_id': account_id, 'date': date}).mappings().all()

        return jsonify({'ok': True, 'data': [enrich_holding(r) for r in result]})

#  2. 即時模擬庫存明細 API
@holding_bp.route('/api/holdings/live', methods=['GET'])
def get_live_holdings():
    account_id = session.get('selected_account_id')
    if not account_id:
        return jsonify({'ok': False, 'error': '缺少 account_id'}), 400

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT h.stock_id, s.symbol, s.name, h.holding_type,
                   h.available_quantity, h.quantity AS total_quantity, h.purchase_price AS avg_price,
                   rs.price AS current_price
            FROM holdings h
            JOIN stocks s ON h.stock_id = s.stock_id
            LEFT JOIN realtime_stock rs ON s.last_price_id = rs.price_id
            WHERE h.account_id = :account_id
        """), {'account_id': account_id}).mappings().all()

        return jsonify({'ok': True, 'data': [enrich_holding(r) for r in result]})
