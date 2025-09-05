from flask import Blueprint, request, jsonify
import mysql.connector
from utils.config import DB_CONFIG

search_tags_api = Blueprint('search_tags_api', __name__)

def build_where_clause(conditions, allowed_fields):
	"""
	將條件陣列轉換為 SQL WHERE 子句與參數
	條件格式: [{field: 'revenue_growth_rate', op: '>', value: 10}]
	"""
	clause = []
	params = []
	for cond in conditions:
		field = cond.get('field')
		op = cond.get('op')
		value = cond.get('value')
		# 安全檢查: 只允許白名單欄位
		if field not in allowed_fields:
			continue
		# 只允許常見運算子
		if op not in ['>', '>=', '<', '<=', '=', '!=', 'BETWEEN', 'IN']:
			continue
		if op == 'BETWEEN' and isinstance(value, list) and len(value) == 2:
			clause.append(f"{field} BETWEEN %s AND %s")
			params.extend(value)
		elif op == 'IN' and isinstance(value, list):
			placeholders = ','.join(['%s'] * len(value))
			clause.append(f"{field} IN ({placeholders})")
			params.extend(value)
		else:
			clause.append(f"{field} {op} %s")
			params.append(value)
	if clause:
		return ' AND '.join(clause), params
	else:
		return '1', []  # 無條件時查全部

@search_tags_api.route('/api/search_tags', methods=['POST'])
def search_tags():
	"""
	1. 先查 stockdb.financial_indicators 取得符合條件的 stock_code
	2. 再查 goodin.stocks 用 symbol 查詢，回傳所有欄位
	"""
	try:
		data = request.get_json()
		symbol = data.get('symbol')
		conditions = data.get('conditions', [])
		limit = data.get('limit')
		if (not symbol) and (not conditions or len(conditions) == 0):
			# 沒有股票代號也沒條件，回傳所有 stocks，支援 limit
			goodin_config = DB_CONFIG.copy()
			goodin_config['database'] = 'goodin'
			conn2 = mysql.connector.connect(**goodin_config)
			cursor2 = conn2.cursor(dictionary=True)
			if limit:
				cursor2.execute("SELECT * FROM stocks LIMIT %s", (int(limit),))
			else:
				cursor2.execute("SELECT * FROM stocks")
			results = cursor2.fetchall()
			cursor2.close()
			conn2.close()
			return jsonify({'ok': True, 'data': results, 'latest_date': None})
		if symbol:
			# 直接查 goodin.stocks
			goodin_config = DB_CONFIG.copy()
			goodin_config['database'] = 'goodin'
			conn2 = mysql.connector.connect(**goodin_config)
			cursor2 = conn2.cursor(dictionary=True)
			cursor2.execute("SELECT * FROM stocks WHERE symbol = %s", (symbol,))
			results = cursor2.fetchall()
			cursor2.close()
			conn2.close()
			return jsonify({'ok': True, 'data': results, 'latest_date': None})

		# 1. 查 stockdb.financial_indicators
		stockdb_config = DB_CONFIG.copy()
		stockdb_config['database'] = 'stockdb'
		allowed_fields = [
			'id', 'stock_code', 'stock_name', 'year_month',
			'revenue_growth_rate', 'net_profit_margin', 'roe_after_tax',
			'free_cash_flow', 'dividend_yield', 'debt_ratio',
			'created_at', 'updated_at'
		]
		where_clause, params = build_where_clause(conditions, allowed_fields)
		conn1 = mysql.connector.connect(**stockdb_config)
		cursor1 = conn1.cursor(dictionary=True)

		# 查詢最新 year_month
		cursor1.execute("SELECT `year_month` FROM financial_indicators ORDER BY `year_month` DESC LIMIT 1")
		latest_date_row = cursor1.fetchone()
		latest_date = latest_date_row['year_month'] if latest_date_row and latest_date_row['year_month'] else None

		# 強制條件只查最新 year_month
		if latest_date:
			where_clause = f"({where_clause}) AND `year_month` = %s"
			params = params + [latest_date]
		else:
			# 沒有資料直接回傳
			return jsonify({'ok': True, 'data': [], 'latest_date': None})

		# 查詢符合條件的股票代碼（僅最新 year_month）
		query1 = f"SELECT stock_code FROM financial_indicators WHERE {where_clause}"
		cursor1.execute(query1, params)
		codes = [row['stock_code'] for row in cursor1.fetchall()]
		cursor1.close()
		conn1.close()

		if not codes:
			return jsonify({'ok': True, 'data': [], 'latest_date': latest_date})

		# 2. 查 goodin.stocks
		goodin_config = DB_CONFIG.copy()
		goodin_config['database'] = 'goodin'
		conn2 = mysql.connector.connect(**goodin_config)
		cursor2 = conn2.cursor(dictionary=True)
		placeholders = ','.join(['%s'] * len(codes))
		query2 = f"SELECT * FROM stocks WHERE symbol IN ({placeholders})"
		cursor2.execute(query2, codes)
		results = cursor2.fetchall()
		cursor2.close()
		conn2.close()

		return jsonify({'ok': True, 'data': results, 'latest_date': latest_date})
	except Exception as e:
		# 若發生例外，也查詢一次最新日期
		latest_date = None
		try:
			stockdb_config = DB_CONFIG.copy()
			stockdb_config['database'] = 'stockdb'
			conn1 = mysql.connector.connect(**stockdb_config)
			cursor1 = conn1.cursor(dictionary=True)
			cursor1.execute("SELECT year_month FROM financial_indicators ORDER BY year_month DESC LIMIT 1")
			latest_date_row = cursor1.fetchone()
			latest_date = latest_date_row['year_month'] if latest_date_row and latest_date_row['year_month'] else None
			cursor1.close()
			conn1.close()
		except Exception:
			latest_date = None
		return jsonify({'ok': False, 'error': str(e), 'latest_date': latest_date}), 500
