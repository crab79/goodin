from flask import Flask, render_template

app = Flask(__name__)

# 首頁
@app.route('/')
def index():
    return render_template('settings.html')  

# Components
@app.route('/buttons')
def buttons():
    return '<h1>Buttons page (未完成)</h1>'

@app.route('/cards')
def cards():
    return '<h1>Cards page (未完成)</h1>'

# Utilities
@app.route('/utilities-color')
def utilities_color():
    return '<h1>Utilities - Color</h1>'

@app.route('/utilities-border')
def utilities_border():
    return '<h1>Utilities - Border</h1>'

@app.route('/utilities-animation')
def utilities_animation():
    return '<h1>Utilities - Animation</h1>'

@app.route('/utilities-other')
def utilities_other():
    return '<h1>Utilities - Other</h1>'

# Pages - Login 系列
@app.route('/login')
def login():
    return '<h1>Login Page</h1>'

@app.route('/register')
def register():
    return '<h1>Register Page</h1>'

@app.route('/forgot-password')
def forgot_password():
    return '<h1>Forgot Password Page</h1>'

# Pages - 其他
@app.route('/404')
def not_found():
    return '<h1>404 Page</h1>'

@app.route('/blank')
def blank():
    return '<h1>Blank Page</h1>'

# Charts & Tables
@app.route('/charts')
def charts():
    return '<h1>Charts Page</h1>'

@app.route('/tables')
def tables():
    return '<h1>Tables Page</h1>'

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

@app.route('/account-overview')
def account_overview():
    return render_template('帳戶概覽.html')

@app.route('/edit-profile')
def edit_profile():
    return render_template('edit-profile.html')

@app.route("/smart-analysis")
def smart_analysis():
    return render_template("smart_analysis.html")

@app.route("/history_account")
def history_account():
    return render_template("history_account.html")


# 執行 Flask
if __name__ == '__main__':
    app.run(debug=True)
