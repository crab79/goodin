from flask import Flask, render_template

app = Flask(__name__, 
            static_folder='static',  # 這裡設為你的 static 資料夾路徑
            template_folder='templates')  # 這裡設為你的 templates 資料夾路徑

@app.route('/')
def index():
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

if __name__ == '__main__':
    app.run(debug=True)
