from flask import Flask, render_template

app = Flask(__name__, 
            static_folder='static',  # 這裡設為你的 static 資料夾路徑
            template_folder='templates')  # 這裡設為你的 templates 資料夾路徑

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visitor')
def visitor():
    return render_template('visitor.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/password')
def password():
    return render_template('password.html')
    
@app.route('/stock_class')
def stock_class():
    return render_template('stock_class.html')

@app.route('/learning_analysis')
def learning_analysis():
    return render_template('learning_analysis.html')

@app.route('/practice_selection')
def practice_selection():
    return render_template('practice_selection.html')

@app.route('/course_selection')
def course_selection():
    return render_template('course_selection.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/search_tag')
def search_tag():
    return render_template('search_tag.html')

@app.route('/StockTrendChart')
def StockTrendChart():
    return render_template('StockTrendChart.html')

@app.route('/chooseaccount')
def chooseaccount():
    return render_template('chooseAccount.html')

@app.route('/exercise_index')
def exercise_index():
    return render_template('exercise_index.html')

@app.route('/historical')
def historical():
    return render_template('historical.html')

@app.route('/historical_function')
def historical_function():
    return render_template('historical_function.html')

@app.route('/historical_trade_history')
def historical_trade_history():
    return render_template('historical_trade_history.html')

@app.route('/pal_calc')
def pal_calc():
    return render_template('pal_calc.html')

@app.route('/order_status')
def order_status():
    return render_template('order_status.html')

@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

@app.route('/realtime_function')
def realtime_function():
    return render_template('realtime_function.html')

@app.route('/realtime_list')
def realtime_list():
    return render_template('realtime_list.html')

@app.route('/realtime_trade_history')
def realtime_trade_history():
    return render_template('realtime_trade_history.html')

if __name__ == '__main__':
    app.run(debug=True)
