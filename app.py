import os
from flask import Flask, render_template
from flask import request
from flask_cors import CORS
from dotenv import load_dotenv
from api.course1_api import course1_api
from api.course2_api import course2_api
from api.course3_api import course3_api
from api.course4_api import course4_api
from api.course5_api import course5_api
from api.course6_api import course6_api
from api.course7_api import course7_api
from api.course8_api import course8_api
from api.course9_api import course9_api
from api.choose_account import choose_account_api
from api.progress_api import progress_api
from api.daily_news import daily_news_api
from api.search_tags import search_tags_api

# 根據環境載入對應的 .env 檔案
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env')

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

CORS(app)


app.register_blueprint(course1_api)
app.register_blueprint(course2_api)
app.register_blueprint(course3_api)
app.register_blueprint(course4_api)
app.register_blueprint(course5_api)
app.register_blueprint(course6_api)
app.register_blueprint(course7_api)
app.register_blueprint(course8_api)
app.register_blueprint(course9_api)
app.register_blueprint(choose_account_api)
app.register_blueprint(progress_api)
app.register_blueprint(daily_news_api)
app.register_blueprint(search_tags_api)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/member_home')
def member_home():
    return render_template('member_home.html')

@app.route('/visitor_home')
def visitor_home():
    return render_template('visitor_home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/find_password')
def find_password():
    return render_template('find_password.html')

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

@app.route('/order_page_realtime')
def order_page_realtime():
    return render_template('order_page_realtime.html')

@app.route('/order_page_history')
def order_page_history():
    return render_template('order_page_history.html')

@app.route('/exercise_index')
def exercise_index():
    return render_template('exercise_index.html')

@app.route('/history_account')
def history_account():
    return render_template('history_account.html')

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

# 個人資料頁
@app.route('/profile')
def profile():
    return render_template('profile.html')
# @app.route('/profile')
# def profile():
#     user = {
#         "member_id": "3024001",
#         "name": "劉小明",
#         "gender": "男",
#         "phone": "0917-171717",
#         "email": "www@gmail.com",
#         "avatar": None  # 或指定圖片檔名，例如 'avatar.jpg'
#     }
#     return render_template('profile.html', user=user)

@app.route('/account_overview')
def account_overview():
    return render_template('account_overview.html')

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')  


@app.route('/course1')
def course1():
    return render_template('course1.html')

@app.route('/practice1')
def practice1():
    return render_template('practice1.html')

@app.route('/course2')
def course2():
    return render_template('course2.html')

@app.route('/practice2')
def practice2():
    return render_template('practice2.html')

@app.route('/course3')
def course3():
    return render_template('course3.html')

@app.route('/practice3')
def practice3():
    return render_template('practice3.html')

@app.route('/course4')
def course4():
    return render_template('course4.html')

@app.route('/practice4')
def practice4():
    return render_template('practice4.html')

@app.route('/course5')
def course5():
    return render_template('course5.html')

@app.route('/practice5')
def practice5():
    return render_template('practice5.html')

@app.route('/course6')
def course6():
    return render_template('course6.html')

@app.route('/practice6')
def practice6():
    return render_template('practice7.html')

@app.route('/course7')
def course7():
    return render_template('course7.html')  

@app.route('/practice7')
def practice7():
    return render_template('practice7.html')

@app.route('/course8')
def course8():
    return render_template('course8.html')

@app.route('/practice8')
def practice8():
    return render_template('practice8.html')

@app.route('/course9')
def course9():
    return render_template('course9.html')

@app.route('/practice9')
def practice9():
    return render_template('practice9.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/smart_analysis')
def smart_analysis():
    return render_template('smart_analysis.html')

@app.route('/choose_account')
@app.route('/choose_account.html')
def choose_account():
    account_type = request.args.get('type', 'default')
    return render_template('choose_account.html', account_type=account_type)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # 允許外部訪問
        port=8000,       
        debug=True
    )
