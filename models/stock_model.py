from models.db import get_db_connection

class StockModel:
    def get_stock(self, symbol):
        conn = get_db_connection()
        if not conn:
            return {"error": "DB connection failed"}
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stocks WHERE symbol = %s", (symbol,))
        stock = cursor.fetchone()
        conn.close()
        return stock or {"symbol": symbol, "name": "Unknown", "current_price": 0.0}

    def add_stock(self, stock_id, symbol, name, sector, market_cap, current_price):
        conn = get_db_connection()
        if not conn:
            return {"error": "DB connection failed"}
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO stocks (stock_id, symbol, name, sector, market_cap, current_price)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                symbol = VALUES(symbol),
                name = VALUES(name),
                sector = VALUES(sector),
                market_cap = VALUES(market_cap),
                current_price = VALUES(current_price)
        ''', (stock_id, symbol, name, sector, market_cap, current_price))
        conn.commit()
        conn.close()
        return {"stock_id": stock_id, "symbol": symbol, "name": name}

    def get_all_stocks(self):
        conn = get_db_connection()
        if not conn:
            return {"error": "DB connection failed"}
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stocks")
        stocks = cursor.fetchall()
        conn.close()
        return stocks
