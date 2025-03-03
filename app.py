from flask import Flask, render_template
from flask_restful import Api
from api.stock_api import StockAPI
from models.stock_model import StockModel

app = Flask(__name__)
api = Api(app)

api.add_resource(StockAPI, '/api/stock')

@app.route('/')
def index():
    stock_model = StockModel()
    stocks = stock_model.get_all_stocks()
    return render_template('index.html', stocks=stocks)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
