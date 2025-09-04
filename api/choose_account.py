from flask import Blueprint, request, jsonify, session
import mysql.connector
from models.db import get_db_connection
from datetime import datetime
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 創建藍圖
choose_account_api = Blueprint('choose_account_api', __name__)

@choose_account_api.route('/api/simulated-accounts', methods=['GET'])
def get_simulated_accounts():
    """
    取得使用者的模擬帳號列表
    """
    try:
        # 從 session 取得 user_id
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'message': '使用者未登入'
            }), 401
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': '資料庫連接失敗'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # 查詢使用者的模擬帳號
        query = """
            SELECT account_id, user_id, account_type, cash, account_name, created_at
            FROM simulated_account 
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        
        cursor.execute(query, (user_id,))
        accounts = cursor.fetchall()
        
        # 轉換數據格式
        account_list = []
        for account in accounts:
            account_list.append({
                'saccount_id': account['account_id'],
                'user_id': account['user_id'],
                'account_type': account['account_type'],
                'cash': float(account['cash']) if account['cash'] else 0.0,
                'account_name': account.get('account_name', f"帳號 {account['account_id']}"),
                'created_at': account.get('created_at').isoformat() if account.get('created_at') else None
            })
        
        cursor.close()
        conn.close()
        
        logger.info(f"成功取得使用者 {user_id} 的 {len(account_list)} 個帳號")
        
        return jsonify({
            'success': True,
            'accounts': account_list
        })
        
    except mysql.connector.Error as e:
        logger.error(f"資料庫錯誤: {e}")
        return jsonify({
            'success': False,
            'message': f'資料庫錯誤: {str(e)}'
        }), 500
    except Exception as e:
        logger.error(f"未預期的錯誤: {e}")
        return jsonify({
            'success': False,
            'message': f'伺服器錯誤: {str(e)}'
        }), 500

@choose_account_api.route('/api/create-simulated-account', methods=['POST'])
def create_simulated_account():
    """
    建立新的模擬帳號
    """
    try:
        data = request.get_json()
        
        # 驗證必要欄位
        required_fields = ['account_name', 'account_type', 'initial_cash']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'缺少必要欄位: {field}'
                }), 400
        
        account_name = data['account_name'].strip()
        account_type = data['account_type']
        initial_cash = float(data['initial_cash'])
        
        # 驗證帳號類型
        if account_type not in ['realtime', 'history']:
            return jsonify({
                'success': False,
                'message': '無效的帳號類型'
            }), 400
        
        # 驗證初始資金
        if initial_cash < 1000 or initial_cash > 10000000:
            return jsonify({
                'success': False,
                'message': '初始資金必須在 1,000 到 10,000,000 之間'
            }), 400
        
        # 驗證帳號名稱長度
        if len(account_name) > 50:
            return jsonify({
                'success': False,
                'message': '帳號名稱不能超過 50 個字元'
            }), 400
        
        # 從 session 取得 user_id
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'message': '使用者未登入'
            }), 401
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': '資料庫連接失敗'
            }), 500
        
        cursor = conn.cursor()
        
        # 檢查帳號名稱是否已存在（同一使用者）
        check_query = """
            SELECT COUNT(*) as count 
            FROM simulated_account 
            WHERE user_id = %s AND account_name = %s
        """
        cursor.execute(check_query, (user_id, account_name))
        result = cursor.fetchone()
        
        if result[0] > 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': '帳號名稱已存在，請使用其他名稱'
            }), 400
        
        # 插入新帳號
        insert_query = """
            INSERT INTO simulated_account (user_id, account_type, cash, account_name, created_at) 
            VALUES (%s, %s, %s, %s, %s)
        """
        
        current_time = datetime.now()
        cursor.execute(insert_query, (user_id, account_type, initial_cash, account_name, current_time))
        
        # 取得新建立的帳號 ID
        new_account_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"成功建立帳號: user_id={user_id}, account_id={new_account_id}, name={account_name}")
        
        return jsonify({
            'success': True,
            'message': '帳號建立成功',
            'account_id': new_account_id
        })
        
    except ValueError as e:
        logger.error(f"數值轉換錯誤: {e}")
        return jsonify({
            'success': False,
            'message': '初始資金必須是有效的數字'
        }), 400
    except mysql.connector.Error as e:
        logger.error(f"資料庫錯誤: {e}")
        return jsonify({
            'success': False,
            'message': f'資料庫錯誤: {str(e)}'
        }), 500
    except Exception as e:
        logger.error(f"未預期的錯誤: {e}")
        return jsonify({
            'success': False,
            'message': f'伺服器錯誤: {str(e)}'
        }), 500

@choose_account_api.route('/api/select-account', methods=['POST'])
def select_account():
    """
    選擇帳號並儲存到 session
    """
    try:
        # 從 session 取得 user_id
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'message': '使用者未登入'
            }), 401
            
        data = request.get_json()
        
        if 'account_id' not in data:
            return jsonify({
                'success': False,
                'message': '缺少帳號 ID'
            }), 400
        
        account_id = int(data['account_id'])
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': '資料庫連接失敗'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # 驗證帳號是否存在且屬於該使用者
        verify_query = """
            SELECT account_id, account_name, account_type, cash
            FROM simulated_account 
            WHERE account_id = %s AND user_id = %s
        """
        
        cursor.execute(verify_query, (account_id, user_id))
        account = cursor.fetchone()
        
        if not account:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': '找不到指定的帳號或無權限訪問'
            }), 404
        
        # 將選擇的帳號資訊儲存到 session
        session['selected_account_id'] = account_id
        session['selected_account_type'] = account['account_type']
        session['selected_account_name'] = account['account_name']
        session['selected_account_cash'] = float(account['cash'])
        
        cursor.close()
        conn.close()
        
        logger.info(f"使用者 {user_id} 選擇了帳號 {account_id} ({account['account_name']})")
        
        return jsonify({
            'success': True,
            'message': '帳號選擇成功',
            'account': {
                'saccount_id': account['account_id'],
                'account_name': account['account_name'],
                'account_type': account['account_type'],
                'cash': float(account['cash'])
            }
        })
        
    except ValueError as e:
        logger.error(f"數值轉換錯誤: {e}")
        return jsonify({
            'success': False,
            'message': '無效的帳號 ID'
        }), 400
    except mysql.connector.Error as e:
        logger.error(f"資料庫錯誤: {e}")
        return jsonify({
            'success': False,
            'message': f'資料庫錯誤: {str(e)}'
        }), 500
    except Exception as e:
        logger.error(f"未預期的錯誤: {e}")
        return jsonify({
            'success': False,
            'message': f'伺服器錯誤: {str(e)}'
        }), 500

@choose_account_api.route('/api/current-account', methods=['GET'])
def get_current_account():
    """
    取得當前選擇的帳號資訊
    """
    try:
        # 從 session 取得 user_id
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'message': '使用者未登入'
            }), 401
            
        if 'selected_account_id' not in session:
            return jsonify({
                'success': False,
                'message': '未選擇帳號'
            }), 400
        
        return jsonify({
            'success': True,
            'account': {
                'saccount_id': session['selected_account_id'],
                'account_name': session.get('selected_account_name', ''),
                'account_type': session.get('selected_account_type', ''),
                'cash': session.get('selected_account_cash', 0.0)
            }
        })
        
    except Exception as e:
        logger.error(f"未預期的錯誤: {e}")
        return jsonify({
            'success': False,
            'message': f'伺服器錯誤: {str(e)}'
        }), 500