from flask_restful import Resource, request
from models.stock_model import StockModel

class StockAPI(Resource):
    def __init__(self):
        self.model = StockModel()

    def get(self):
        symbol = request.args.get("symbol", "2330")
        stock = self.model.get_stock(symbol)
        return {
            "stock_id": stock.get("stock_id"),
            "symbol": stock["symbol"],
            "name": stock["name"],
            "sector": stock.get("sector"),
            "market_cap": float(stock.get("market_cap", 0)),
            "current_price": float(stock["current_price"])
        }

    def post(self):
        data = request.get_json()
        stock_id = data["stock_id"]
        symbol = data["symbol"]
        name = data["name"]
        sector = data.get("sector")
        market_cap = data.get("market_cap", 0)
        current_price = data["current_price"]
        result = self.model.add_stock(stock_id, symbol, name, sector, market_cap, current_price)
        return {"message": f"Added/Updated stock: {symbol}", "stock": result}, 201
