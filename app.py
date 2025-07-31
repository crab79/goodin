from flask import Flask, render_template

app = Flask(__name__, 
            static_folder='static',  # 這裡設為你的 static 資料夾路徑
            template_folder='templates')  # 這裡設為你的 templates 資料夾路徑

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

@app.route('/search_tag')
def search_tag():
    return render_template('search_tag.html')

@app.route('/order_page_realtime')
def order_page_realtime():
    return render_template('order_page_realtime.html')

@app.route('/order_page_history')
def order_page_history():
    return render_template('order_page_history.html')

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


if __name__ == '__main__':
    app.run(debug=True)
