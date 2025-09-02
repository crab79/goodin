from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__, static_folder='C:/Users/angel/OneDrive/桌面/frontend_workspace/my_flask_app/static', template_folder='C:/Users/angel/OneDrive/桌面/frontend_workspace/my_flask_app/templates')

# MySQL 連線設定
db_config = {
    'host': '140.127.220.85',
    'user': 'nukim',
    'password': 'nukim',
    'database': 'stockdb'
}

@app.route('/')
def index():
    return render_template('realtime.html')

@app.route('/financials')
def financials():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 只選取你要的六個欄位
    query = """
    SELECT `營收成長率`, `稅後淨利率`, `ROE(A)－稅後`, 
           `自由現金流量(D)`, `股利殖利率`, `負債比率`
    FROM financials;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
