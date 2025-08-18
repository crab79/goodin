from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
today = datetime.now()


# 假資料
fake_courses = [
    {'course_id': 1, 'title': '課程介紹+技術分析概述'},
    {'course_id': 2, 'title': '基本面分析概述'},
    {'course_id': 3, 'title': 'K線圖和價格型態'},
    {'course_id': 4, 'title': '簡單移動平均線（SMA）'},
    {'course_id': 5, 'title': '相對強弱指數（RSI）'},
    {'course_id': 6, 'title': '布林帶（Bollinger Bands）'},
    {'course_id': 7, 'title': 'MACD'},
    {'course_id': 8, 'title': 'KD指標（Stochastic Oscillator）'},
    {'course_id': 9, 'title': '乖離率（BIAS）'},
]
fake_user_course_progress = [
    {'user_id': 1, 'course_id': 1, 'completed_at': '2025-08-01'},
    {'user_id': 1, 'course_id': 2, 'completed_at': '2025-08-02'},
    {'user_id': 1, 'course_id': 3, 'completed_at': '2025-08-03'},
    {'user_id': 1, 'course_id': 4, 'completed_at': '2025-08-04'},
    {'user_id': 1, 'course_id': 5, 'completed_at': '2025-08-05'},
    {'user_id': 1, 'course_id': 6, 'completed_at': '2025-08-06'},
    {'user_id': 1, 'course_id': 7, 'completed_at': '2025-08-07'},
    {'user_id': 1, 'course_id': 8, 'completed_at': '2025-08-08'},
]
fake_user_practice_progress = [
    # 課程1: 課程介紹+技術分析概述
    {'user_id': 1, 'exercise_id': 11, 'course_id': 1, 'completed_at': '2025-08-01', 'total_questions': 5, 'correct_answers': 4, 'accuracy_rate': 80.0},
    {'user_id': 1, 'exercise_id': 12, 'course_id': 1, 'completed_at': '2025-08-01', 'total_questions': 3, 'correct_answers': 3, 'accuracy_rate': 100.0},
    
    # 課程2: 基本面分析概述
    {'user_id': 1, 'exercise_id': 21, 'course_id': 2, 'completed_at': '2025-08-02', 'total_questions': 5, 'correct_answers': 3, 'accuracy_rate': 60.0},
    {'user_id': 1, 'exercise_id': 22, 'course_id': 2, 'completed_at': '2025-08-02', 'total_questions': 4, 'correct_answers': 4, 'accuracy_rate': 100.0},
    
    # 課程3: K線圖和價格型態
    {'user_id': 1, 'exercise_id': 31, 'course_id': 3, 'completed_at': '2025-08-03', 'total_questions': 5, 'correct_answers': 5, 'accuracy_rate': 100.0},
    {'user_id': 1, 'exercise_id': 32, 'course_id': 3, 'completed_at': '2025-08-03', 'total_questions': 3, 'correct_answers': 2, 'accuracy_rate': 66.7},
    
    # 課程4: 簡單移動平均線（SMA）
    {'user_id': 1, 'exercise_id': 41, 'course_id': 4, 'completed_at': '2025-08-04', 'total_questions': 6, 'correct_answers': 4, 'accuracy_rate': 66.7},
    
    # 課程5: 相對強弱指數（RSI）
    {'user_id': 1, 'exercise_id': 51, 'course_id': 5, 'completed_at': '2025-08-05', 'total_questions': 5, 'correct_answers': 4, 'accuracy_rate': 80.0},
    
    # 課程6: 布林帶（Bollinger Bands）
    {'user_id': 1, 'exercise_id': 61, 'course_id': 6, 'completed_at': '2025-08-06', 'total_questions': 5, 'correct_answers': 3, 'accuracy_rate': 60.0},
    
    # 課程7: MACD
    {'user_id': 1, 'exercise_id': 71, 'course_id': 7, 'completed_at': '2025-08-07', 'total_questions': 4, 'correct_answers': 4, 'accuracy_rate': 100.0},
    
    # 課程8: KD指標（Stochastic Oscillator）
    {'user_id': 1, 'exercise_id': 81, 'course_id': 8, 'completed_at': '2025-08-08', 'total_questions': 6, 'correct_answers': 5, 'accuracy_rate': 83.3},
    
]
fake_practice_errors = [
    # 課程2錯誤範例: 基本面分析概述
    {
        'practice_id': 21,  # 對應 exercise_id
        'user_id': 1,
        'question_id': 201,
        'question_text': '基本面分析主要關注哪些方面？',
        'user_option_code': 'A',
        'user_option_text': '技術指標和圖表型態',
        'correct_option_code': 'B',
        'correct_option_text': '公司財務狀況和經營績效',
    },
    # 課程3錯誤範例: K線圖和價格型態
    {
        'practice_id': 32,  # 對應 exercise_id
        'user_id': 1,
        'question_id': 301,
        'question_text': 'K線的實體部分代表什麼？',
        'user_option_code': 'A',
        'user_option_text': '最高價與最低價',
        'correct_option_code': 'B',
        'correct_option_text': '開盤價與收盤價',
    },
    # 課程4錯誤範例: 簡單移動平均線（SMA）
    {
        'practice_id': 41,  # 對應 exercise_id
        'user_id': 1,
        'question_id': 401,
        'question_text': 'SMA 的計算方式是什麼？',
        'user_option_code': 'C',
        'user_option_text': '加權平均',
        'correct_option_code': 'A',
        'correct_option_text': '算術平均',
    },
    {
        'practice_id': 41,  # 同一個練習的另一個錯誤
        'user_id': 1,
        'question_id': 402,
        'question_text': 'SMA 5 和 SMA 20 哪個反應比較快？',
        'user_option_code': 'B',
        'user_option_text': 'SMA 20',
        'correct_option_code': 'A',
        'correct_option_text': 'SMA 5',
    },
    # 課程5錯誤範例: 相對強弱指數（RSI）
    {
        'practice_id': 51,  # 對應 exercise_id
        'user_id': 1,
        'question_id': 501,
        'question_text': 'RSI 超過 70 通常表示什麼？',
        'user_option_code': 'B',
        'user_option_text': '超賣訊號',
        'correct_option_code': 'A',
        'correct_option_text': '超買訊號',
    },
    # 課程6錯誤範例: 布林帶（Bollinger Bands）
    {
        'practice_id': 61,  # 對應 exercise_id
        'user_id': 1,
        'question_id': 601,
        'question_text': '布林帶的組成包括哪些？',
        'user_option_code': 'B',
        'user_option_text': '上軌、中軌',
        'correct_option_code': 'A',
        'correct_option_text': '上軌、中軌、下軌',
    },
    {
        'practice_id': 61,  # 同一個練習的另一個錯誤
        'user_id': 1,
        'question_id': 602,
        'question_text': '布林帶的標準差是多少？',
        'user_option_code': 'A',
        'user_option_text': '1',
        'correct_option_code': 'B',
        'correct_option_text': '2',
    },
]

# 完成課程（接收實際課程完成資料）
@app.route('/api/complete_course', methods=['POST'])
def complete_course():
    try:
        data = request.get_json()
        
        # 驗證必需欄位
        required_fields = ['user_id', 'course_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
        
        # 統一處理 user_id
        user_id = 1 if data['user_id'] == 'default_user' else data['user_id']
        course_id = data['course_id']
        
        # 檢查課程是否已完成
        existing_record = next((r for r in fake_user_course_progress 
                               if r['user_id'] == user_id and r['course_id'] == course_id), None)
        
        if existing_record:
            return jsonify({
                'status': 'success',
                'message': '課程已經完成',
                'completed_at': existing_record['completed_at']
            })
        
        # 建立課程完成記錄
        course_record = {
            'user_id': user_id,
            'course_id': course_id,
            'completed_at': data.get('completed_at', datetime.now().strftime('%Y-%m-%d'))
        }
        
        # 新增到假資料中（實際應存入資料庫）
        fake_user_course_progress.append(course_record)
        
        print(f"課程完成記錄已保存: User {data['user_id']}, Course {data['course_id']}")
        
        return jsonify({
            'status': 'success',
            'message': '課程完成記錄已保存',
            'completed_at': course_record['completed_at']
        })
        
    except Exception as e:
        print(f"保存課程完成記錄時發生錯誤: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 完成練習（接收實際測驗結果）
@app.route('/api/complete_practice', methods=['POST'])
def complete_practice():
    try:
        data = request.get_json()
        
        # 驗證必需欄位
        required_fields = ['user_id', 'exercise_id', 'course_id', 'total_questions', 'correct_answers', 'accuracy_rate']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
        
        # 統一處理 user_id
        user_id = 1 if data['user_id'] == 'default_user' else data['user_id']
        
        # 建立練習記錄
        practice_record = {
            'user_id': user_id,
            'exercise_id': data['exercise_id'],
            'course_id': data['course_id'],
            'completed_at': data.get('completed_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'total_questions': data['total_questions'],
            'correct_answers': data['correct_answers'],
            'accuracy_rate': data['accuracy_rate'],
            'exercise_type': data.get('exercise_type', 'choice'),  # 'choice' 或 'chart'
            'duration_seconds': data.get('duration_seconds'),  # 作答總時間（秒）
            'started_at': data.get('started_at'),  # 開始時間
        }
        
        # 新增到假資料中（實際應存入資料庫）
        fake_user_practice_progress.append(practice_record)
        
        # 處理錯誤題目
        errors = data.get('errors', [])
        practice_id = len(fake_user_practice_progress)  # 簡單的ID生成
        
        for error in errors:
            error_record = {
                'practice_id': practice_id,
                'user_id': user_id,  # 使用統一處理後的 user_id
                'question_id': error.get('question_id'),
                'question_number': error.get('question_number'),
                'question_text': error.get('question_text'),
                'question_description': error.get('question_description', ''),
                'question_options': error.get('question_options', []),
                'user_option_code': error.get('user_option_code'),
                'user_option_text': error.get('user_option_text'),
                'correct_option_code': error.get('correct_option_code'),
                'correct_option_text': error.get('correct_option_text'),
                'explanation': error.get('explanation', ''),
                'answer_duration': error.get('answer_duration', 0),  # 單題作答時間（秒）
                'answered_at': error.get('answered_at'),  # 答題時間
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            fake_practice_errors.append(error_record)
        
        print(f"練習完成記錄已保存: User {user_id}, Exercise {data['exercise_id']}, 正確率: {data['accuracy_rate']:.1f}%, 類型: {data.get('exercise_type', 'choice')}")
        if data.get('duration_seconds'):
            print(f"作答時間: {data['duration_seconds']} 秒")
        
        return jsonify({
            'status': 'success',
            'message': '練習結果已成功保存',
            'practice_id': practice_id,
            'accuracy_rate': data['accuracy_rate'],
            'duration_seconds': data.get('duration_seconds'),
            'errors_count': len(errors)
        })
        
    except Exception as e:
        print(f"保存練習結果時發生錯誤: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 學習成效分析總覽（假資料）
@app.route('/api/learning_analytics/<int:user_id>', methods=['GET'])
def learning_analytics(user_id):
    completed_courses = [p for p in fake_user_course_progress if p['user_id'] == user_id]
    total_courses = len(fake_courses)
    course_progress = round(len(completed_courses) / total_courses * 100, 1) if total_courses > 0 else 0
    latest_course = completed_courses[-1]['course_id'] if completed_courses else None
    latest_course_title = next((c['title'] for c in fake_courses if c['course_id'] == latest_course), None)
    
    # 平均練習正確率
    user_practices = [p for p in fake_user_practice_progress if p['user_id'] == user_id]
    avg_accuracy = round(sum(p['accuracy_rate'] for p in user_practices) / len(user_practices), 1) if user_practices else 0
    total_practices = len(user_practices)
    
    # 學習頻率
    study_dates = sorted([p['completed_at'] for p in completed_courses] + [p['completed_at'] for p in user_practices], reverse=True)
    week_ago = '2025-07-31'
    recent_studies = len([d for d in study_dates if d >= week_ago])
    last_study = study_dates[0] if study_dates else None
    
    # streak 計算（字串日期）
    def strdate_streak(dates):
        if not dates:
            return 0
        streak = 1
        current = dates[0]
        for i in range(1, len(dates)):
            prev = dates[i]
            # 轉 datetime 比較
            from datetime import datetime
            cdt = datetime.strptime(current, '%Y-%m-%d')
            pdt = datetime.strptime(prev, '%Y-%m-%d')
            if (cdt - pdt).days == 1:
                streak += 1
                current = prev
            else:
                break
        return streak
    streak = strdate_streak(study_dates)
    
    # 課程詳細進度
    course_details = []
    for course in fake_courses:
        is_completed = any(c['course_id'] == course['course_id'] for c in completed_courses)
        course_practices = [p for p in user_practices if p['course_id'] == course['course_id']]
        avg_course_accuracy = round(sum(p['accuracy_rate'] for p in course_practices) / len(course_practices), 1) if course_practices else 0
        
        course_details.append({
            'course_id': course['course_id'],
            'title': course['title'],
            'completed': is_completed,
            'completed_at': next((c['completed_at'] for c in completed_courses if c['course_id'] == course['course_id']), None),
            'practice_count': len(course_practices),
            'avg_accuracy': avg_course_accuracy
        })
    
    return jsonify({
        'course_progress': {
            'percentage': course_progress,
            'completed': len(completed_courses),
            'total': total_courses,
            'latest_course': latest_course_title,
            'latest_course_id': latest_course
        },
        'practice_stats': {
            'avg_accuracy': avg_accuracy,
            'total_practices': total_practices
        },
        'learning_frequency': {
            'recent_7_days': recent_studies,
            'last_study_date': last_study,
            'consecutive_days': streak
        },
        'course_details': course_details
    })

# 獲取特定課程詳細資訊
@app.route('/api/course_info/<int:course_id>', methods=['GET'])
def get_course_info(course_id):
    course = next((c for c in fake_courses if c['course_id'] == course_id), None)
    if not course:
        return jsonify({'status': 'error', 'message': '課程不存在'}), 404
    
    # 獲取課程相關的練習統計
    course_practices = [p for p in fake_user_practice_progress if p['course_id'] == course_id]
    total_practices = len(course_practices)
    avg_accuracy = round(sum(p['accuracy_rate'] for p in course_practices) / len(course_practices), 1) if course_practices else 0
    
    return jsonify({
        'course_id': course['course_id'],
        'title': course['title'],
        'practice_stats': {
            'total_practices': total_practices,
            'avg_accuracy': avg_accuracy
        }
    })

# 獲取用戶特定課程的學習狀態
@app.route('/api/user_course_status/<user_id>/<int:course_id>', methods=['GET'])
def get_user_course_status(user_id, course_id):
    # 如果 user_id 是 "default_user"，轉換為數字 1
    if user_id == "default_user":
        user_id = 1
    else:
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'status': 'error', 'message': '無效的用戶ID'}), 400
    
    # 檢查課程是否存在
    course = next((c for c in fake_courses if c['course_id'] == course_id), None)
    if not course:
        return jsonify({'status': 'error', 'message': '課程不存在'}), 404
    
    # 檢查課程是否已完成
    course_completion = next((c for c in fake_user_course_progress 
                             if c['user_id'] == user_id and c['course_id'] == course_id), None)
    
    # 獲取該課程的練習記錄
    course_practices = [p for p in fake_user_practice_progress 
                       if p['user_id'] == user_id and p['course_id'] == course_id]
    
    # 計算統計資料
    total_practices = len(course_practices)
    avg_accuracy = round(sum(p['accuracy_rate'] for p in course_practices) / len(course_practices), 1) if course_practices else 0
    
    # 獲取錯誤題目
    practice_ids = [p['exercise_id'] for p in course_practices]
    errors = [e for e in fake_practice_errors 
              if e['user_id'] == user_id and e['practice_id'] in practice_ids]
    
    return jsonify({
        'course_info': {
            'course_id': course['course_id'],
            'title': course['title']
        },
        'completion_status': {
            'completed': course_completion is not None,
            'completed_at': course_completion['completed_at'] if course_completion else None
        },
        'practice_stats': {
            'total_practices': total_practices,
            'avg_accuracy': avg_accuracy,
            'practice_details': course_practices
        },
        'errors': errors
    })

# 獲取所有課程列表
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    return jsonify({
        'courses': fake_courses,
        'total_count': len(fake_courses)
    })

# 課堂練習結果分析（假資料）
@app.route('/api/practice_analysis/<int:user_id>', methods=['GET'])
def practice_analysis(user_id):
    user_practices = [p.copy() for p in fake_user_practice_progress if p['user_id'] == user_id]
    for practice in user_practices:
        # 假設 id = exercise_id
        practice['id'] = practice['exercise_id']
        practice['course_name'] = next((c['title'] for c in fake_courses if c['course_id'] == practice['course_id']), '')
        # 趨勢（簡易版）
        practice['trend'] = '—'
        # 錯誤詳情（格式化成前端需要的欄位）
        practice['errors'] = []
        for e in fake_practice_errors:
            # 使用 exercise_id 來對應錯誤資料
            if e['practice_id'] == practice['exercise_id'] and e['user_id'] == user_id:
                practice['errors'].append({
                    'question_id': e.get('question_id'),
                    'question_text': e.get('question_text'),
                    'user_option_code': e.get('user_option_code'),
                    'user_option_text': e.get('user_option_text'),
                    'correct_option_code': e.get('correct_option_code'),
                    'correct_option_text': e.get('correct_option_text'),
                })
        # 格式化數據
        practice['wrong_count'] = practice['total_questions'] - practice['correct_answers']
        practice['error_ratio'] = f"{practice['wrong_count']}/{practice['total_questions']}"
        practice['practice_time'] = practice['completed_at'] + ' 09:00'
        practice.pop('completed_at', None)
    return jsonify({'practices': user_practices})

# 學習建議（假資料）
@app.route('/api/learning_suggestions/<int:user_id>', methods=['GET'])
def learning_suggestions(user_id):
    user_practices = [p for p in fake_user_practice_progress if p['user_id'] == user_id]
    # 各課程平均正確率
    course_stats = []
    course_ids = set(p['course_id'] for p in user_practices)
    for cid in course_ids:
        course_name = next((c['title'] for c in fake_courses if c['course_id'] == cid), '')
        course_practices = [p for p in user_practices if p['course_id'] == cid]
        avg_accuracy = sum(p['accuracy_rate'] for p in course_practices) / len(course_practices)
        course_stats.append({
            'course_name': course_name,
            'avg_accuracy': round(avg_accuracy, 1),
            'practice_count': len(course_practices)
        })
    course_stats.sort(key=lambda x: x['avg_accuracy'])
    # 整體平均正確率
    overall_avg = sum(p['accuracy_rate'] for p in user_practices) / len(user_practices) if user_practices else 0
    suggestions = []
    for course in course_stats:
        if course['avg_accuracy'] < overall_avg:
            suggestions.append({
                'course': course['course_name'],
                'issue': f"平均正確率 {course['avg_accuracy']:.1f}%，低於平均 {overall_avg:.1f}%",
                'suggestion': "建議加強練習"
            })
    return jsonify({
        'overall_average': round(overall_avg, 1),
        'course_stats': course_stats,
        'suggestions': suggestions
    })

def calculate_streak(study_dates):
    if not study_dates:
        return 0
    streak = 1
    current_date = study_dates[0]
    for i in range(1, len(study_dates)):
        prev_date = study_dates[i]
        if (current_date - prev_date).days == 1:
            streak += 1
            current_date = prev_date
        else:
            break
    return streak

# 首頁 - 今日學習成果
@app.route('/api/today_learning/<int:user_id>', methods=['GET'])
def today_learning(user_id):
    try:
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # 查找今日完成的課程
        today_courses = [
            p for p in fake_user_course_progress 
            if p['user_id'] == user_id and p['completed_at'] == today_str
        ]
        
        # 查找今日完成的練習
        today_practices = [
            p for p in fake_user_practice_progress 
            if p['user_id'] == user_id and p['completed_at'].startswith(today_str)
        ]
        
        # 獲取最新完成的課程資訊
        latest_course = None
        if today_courses:
            latest_course_id = today_courses[-1]['course_id']
            course_info = next((c for c in fake_courses if c['course_id'] == latest_course_id), None)
            if course_info:
                latest_course = {
                    'course_id': latest_course_id,
                    'title': course_info['title'],
                    'completed_at': today_courses[-1]['completed_at']
                }
        
        # 獲取最新完成的練習資訊
        latest_practice = None
        if today_practices:
            latest_practice_data = today_practices[-1]
            course_info = next((c for c in fake_courses if c['course_id'] == latest_practice_data['course_id']), None)
            if course_info:
                latest_practice = {
                    'course_id': latest_practice_data['course_id'],
                    'course_title': course_info['title'],
                    'accuracy_rate': latest_practice_data['accuracy_rate'],
                    'completed_at': latest_practice_data['completed_at']
                }
        
        # 決定要顯示的內容
        message = "今天還沒有學習記錄，開始你的學習之旅吧！📚"
        
        if latest_course and latest_practice:
            # 兩者都有，顯示最新的
            if latest_course['completed_at'] >= latest_practice['completed_at'][:10]:
                message = f"完成「第{latest_course['course_id']}課-{latest_course['title']}」，好棒棒！🎉"
            else:
                message = f"完成「第{latest_practice['course_id']}課」練習，正確率 {latest_practice['accuracy_rate']:.0f}%！🎯"
        elif latest_course:
            message = f"完成「第{latest_course['course_id']}課-{latest_course['title']}」，好棒棒！🎉"
        elif latest_practice:
            message = f"完成「第{latest_practice['course_id']}課」練習，正確率 {latest_practice['accuracy_rate']:.0f}%！🎯"
        
        return jsonify({
            'status': 'success',
            'message': message,
            'today_courses_count': len(today_courses),
            'today_practices_count': len(today_practices),
            'latest_course': latest_course,
            'latest_practice': latest_practice
        })
        
    except Exception as e:
        print(f"獲取今日學習成果時發生錯誤: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 首頁 - 課程進度統計
@app.route('/api/course_progress/<int:user_id>', methods=['GET'])
def course_progress(user_id):
    try:
        # 獲取用戶完成的課程
        completed_courses = [
            p for p in fake_user_course_progress 
            if p['user_id'] == user_id
        ]
        
        total_courses = len(fake_courses)
        completed_count = len(completed_courses)
        remaining_count = total_courses - completed_count
        
        # 計算完成百分比
        completion_percentage = round((completed_count / total_courses) * 100, 1) if total_courses > 0 else 0
        
        # 準備圓餅圖資料
        chart_data = {
            'labels': ['已完成', '未完成'],
            'data': [completed_count, remaining_count],
            'colors': ['#4e73df', '#1cc88a'],  # 藍色代表已完成，綠色代表未完成
            'total': total_courses,
            'completed': completed_count,
            'remaining': remaining_count,
            'percentage': completion_percentage
        }
        
        # 獲取完成的課程詳細資訊
        completed_course_details = []
        for progress in completed_courses:
            course_info = next((c for c in fake_courses if c['course_id'] == progress['course_id']), None)
            if course_info:
                completed_course_details.append({
                    'course_id': progress['course_id'],
                    'title': course_info['title'],
                    'completed_at': progress['completed_at']
                })
        
        # 獲取下一個要學習的課程
        next_course = None
        if remaining_count > 0:
            completed_course_ids = [p['course_id'] for p in completed_courses]
            for course in fake_courses:
                if course['course_id'] not in completed_course_ids:
                    next_course = {
                        'course_id': course['course_id'],
                        'title': course['title']
                    }
                    break
        
        return jsonify({
            'status': 'success',
            'chart_data': chart_data,
            'completed_courses': completed_course_details,
            'next_course': next_course,
            'summary': {
                'total_courses': total_courses,
                'completed_count': completed_count,
                'remaining_count': remaining_count,
                'completion_percentage': completion_percentage
            }
        })
        
    except Exception as e:
        print(f"獲取課程進度統計時發生錯誤: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
 app.run(debug=True, port=5001)