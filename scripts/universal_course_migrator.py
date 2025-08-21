#!/usr/bin/env python3
"""
通用課程資料遷移腳本
可以遷移任何課程的資料到資料庫中
"""

import mysql.connector
import json
import sys
import os
import importlib.util

class UniversalCourseMigrator:
    def __init__(self, host='localhost', user='root', password='', database='goodin_learning_platform'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        """連接到資料庫"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            print(f"✅ 成功連接到資料庫: {self.database}")
            return True
        except mysql.connector.Error as err:
            print(f"❌ 資料庫連接失敗: {err}")
            return False
    
    def close(self):
        """關閉資料庫連接"""
        if self.connection:
            self.connection.close()
            print("✅ 資料庫連接已關閉")
    
    def load_course_data(self, course_number):
        """動態載入課程資料"""
        try:
            # 構建檔案路徑
            api_dir = os.path.join(os.path.dirname(__file__), 'api')
            course_file = f'course{course_number}_api.py'
            course_path = os.path.join(api_dir, course_file)
            
            if not os.path.exists(course_path):
                print(f"❌ 找不到課程檔案: {course_path}")
                return None, None
            
            # 動態導入模組
            spec = importlib.util.spec_from_file_location(f"course{course_number}_api", course_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 取得課程頁面資料
            pages_attr = f'course{course_number}_pages'
            if not hasattr(module, pages_attr):
                print(f"❌ 在 {course_file} 中找不到 {pages_attr}")
                return None, None
            
            course_pages = getattr(module, pages_attr)
            print(f"✅ 成功載入課程{course_number}資料，共 {len(course_pages)} 頁")
            
            return course_pages, module
            
        except Exception as e:
            print(f"❌ 載入課程{course_number}資料失敗: {e}")
            return None, None
    
    def get_course_info(self, course_number):
        """取得課程基本資訊"""
        course_info = {
            1: {
                'name': '技術分析入門',
                'description': '學習MACD指標的基本概念與應用，掌握技術分析的核心工具'
            },
            2: {
                'name': '基本面分析',
                'description': '學習如何透過財報數據與經營指標了解企業真實狀況，從獲利、經營、安全與價值四大面向進行分析'
            },
            3: {
                'name': 'K線圖基礎',
                'description': '學習K線圖的基本概念、解讀方法與常見價格型態，了解多空力量變化與市場情緒'
            },
            4: {
                'name': '簡單移動平均線',
                'description': '學習SMA指標的計算方法與應用，掌握黃金交叉與死亡交叉的判斷技巧'
            },
            5: {
                'name': '相對強弱指標 RSI',
                'description': '學習RSI指標的計算公式與應用，掌握超買超賣的判斷技巧與交易訊號'
            },
            6: {
                'name': '布林通道',
                'description': '學習布林通道的結構與應用，掌握波動率指標的判斷技巧與市場收斂擴張訊號'
            },
            7: {
                'name': 'MACD指標進階',
                'description': '深入學習MACD指標的快線慢線與OSC柱狀圖，掌握黃金交叉死亡交叉的進階應用'
            },
            8: {
                'name': 'KD隨機指標',
                'description': '學習KD隨機指標的計算與應用，掌握超買超賣狀況的判斷與黃金交叉死亡交叉訊號'
            },
            9: {
                'name': '乖離率 BIAS',
                'description': '學習乖離率的概念與計算，掌握價格偏離移動平均線的程度判斷與市場節奏分析'
            }
        }
        
        return course_info.get(course_number, {
            'name': f'課程{course_number}',
            'description': f'課程{course_number}的詳細內容'
        })
    
    def insert_course_info(self, course_number, course_info):
        """插入課程基本資訊"""
        cursor = self.connection.cursor()
        
        course_query = """
        INSERT INTO courses (course_id, course_name, course_description, is_active) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        course_name = VALUES(course_name),
        course_description = VALUES(course_description)
        """
        
        course_data = (
            course_number,
            course_info['name'],
            course_info['description'],
            True
        )
        
        try:
            cursor.execute(course_query, course_data)
            self.connection.commit()
            print(f"✅ 課程{course_number}基本資訊插入成功")
            return True
        except mysql.connector.Error as err:
            print(f"❌ 課程資訊插入失敗: {err}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def clear_existing_pages(self, course_number):
        """清除現有的課程頁面資料"""
        cursor = self.connection.cursor()
        
        try:
            cursor.execute("DELETE FROM course_pages WHERE course_id = %s", (course_number,))
            deleted_rows = cursor.rowcount
            self.connection.commit()
            print(f"✅ 清除了 {deleted_rows} 筆現有的課程{course_number}頁面資料")
            return True
        except mysql.connector.Error as err:
            print(f"❌ 清除現有資料失敗: {err}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def insert_course_pages(self, course_number, course_pages):
        """插入課程頁面資料"""
        cursor = self.connection.cursor()
        
        page_query = """
        INSERT INTO course_pages (course_id, page_index, html_content, chart_type, chart_config, multi_steps)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            for page in course_pages:
                # 處理 chart_config 和 multi_steps（如果是字典或列表，轉換為JSON）
                chart_config = None
                if page.get('chart_config'):
                    chart_config = json.dumps(page['chart_config']) if isinstance(page['chart_config'], (dict, list)) else page['chart_config']
                
                multi_steps = None
                if page.get('multi_steps'):
                    multi_steps = json.dumps(page['multi_steps']) if isinstance(page['multi_steps'], (dict, list)) else page['multi_steps']
                
                # 處理 carousel_items（如果存在，合併到 chart_config 中）
                if page.get('carousel_items'):
                    if chart_config:
                        # 如果已有 chart_config，合併 carousel_items
                        config_dict = json.loads(chart_config) if isinstance(chart_config, str) else chart_config or {}
                        config_dict['carousel_items'] = page['carousel_items']
                        chart_config = json.dumps(config_dict)
                    else:
                        # 沒有 chart_config，直接用 carousel_items
                        chart_config = json.dumps({'carousel_items': page['carousel_items']})
                
                page_data = (
                    course_number,  # course_id
                    page['page_index'],
                    page['html_content'],
                    page.get('chart_type'),
                    chart_config,
                    multi_steps
                )
                
                cursor.execute(page_query, page_data)
                print(f"✅ 插入第 {page['page_index']} 頁")
            
            self.connection.commit()
            print(f"✅ 成功插入 {len(course_pages)} 個課程頁面")
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ 頁面資料插入失敗: {err}")
            self.connection.rollback()
            return False
        except Exception as e:
            print(f"❌ 資料處理錯誤: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def verify_data(self, course_number, expected_page_count):
        """驗證插入的資料"""
        cursor = self.connection.cursor()
        
        try:
            # 檢查課程資訊
            cursor.execute("SELECT course_name, course_description FROM courses WHERE course_id = %s", (course_number,))
            course_info = cursor.fetchone()
            if course_info:
                print(f"✅ 課程資訊驗證成功: {course_info[0]}")
            else:
                print("❌ 課程資訊驗證失敗")
                return False
            
            # 檢查頁面數量
            cursor.execute("SELECT COUNT(*) FROM course_pages WHERE course_id = %s", (course_number,))
            page_count = cursor.fetchone()[0]
            
            if page_count == expected_page_count:
                print(f"✅ 頁面數量驗證成功: {page_count}/{expected_page_count}")
            else:
                print(f"❌ 頁面數量不符: {page_count}/{expected_page_count}")
                return False
            
            # 檢查頁面索引完整性
            cursor.execute("SELECT page_index FROM course_pages WHERE course_id = %s ORDER BY page_index", (course_number,))
            page_indexes = [row[0] for row in cursor.fetchall()]
            expected_indexes = list(range(expected_page_count))
            
            if page_indexes == expected_indexes:
                print(f"✅ 頁面索引驗證成功: 0-{expected_page_count-1}")
            else:
                print(f"❌ 頁面索引不完整: {page_indexes}")
                return False
            
            # 檢查特殊功能頁面
            cursor.execute("SELECT page_index, chart_type, multi_steps FROM course_pages WHERE course_id = %s AND (chart_type IS NOT NULL OR multi_steps IS NOT NULL)", (course_number,))
            special_pages = cursor.fetchall()
            if special_pages:
                print(f"✅ 發現 {len(special_pages)} 個包含互動功能的頁面")
                for page_idx, chart_type, multi_steps in special_pages:
                    features = []
                    if chart_type:
                        features.append(f"圖表:{chart_type}")
                    if multi_steps:
                        features.append(f"多步驟顯示")
                    print(f"   第{page_idx}頁: {', '.join(features)}")
            
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ 資料驗證失敗: {err}")
            return False
        finally:
            cursor.close()
    
    def migrate_course(self, course_number):
        """遷移指定課程"""
        print(f"🚀 開始課程{course_number}資料遷移...")
        
        # 載入課程資料
        course_pages, module = self.load_course_data(course_number)
        if not course_pages:
            return False
        
        print(f"📊 預計遷移 {len(course_pages)} 個頁面")
        
        if not self.connect():
            return False
        
        try:
            # 取得課程資訊
            course_info = self.get_course_info(course_number)
            
            # 步驟1：插入課程基本資訊
            if not self.insert_course_info(course_number, course_info):
                return False
            
            # 步驟2：清除現有頁面資料
            if not self.clear_existing_pages(course_number):
                return False
            
            # 步驟3：插入頁面資料
            if not self.insert_course_pages(course_number, course_pages):
                return False
            
            # 步驟4：驗證資料
            if not self.verify_data(course_number, len(course_pages)):
                return False
            
            print(f"🎉 課程{course_number}資料遷移完成！")
            return True
            
        except Exception as e:
            print(f"❌ 遷移過程中發生錯誤: {e}")
            return False
        finally:
            self.close()

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("用法：python universal_course_migrator.py <課程編號>")
        print("例如：python universal_course_migrator.py 3")
        sys.exit(1)
    
    try:
        course_number = int(sys.argv[1])
    except ValueError:
        print("❌ 課程編號必須是數字")
        sys.exit(1)
    
    print("=" * 50)
    print(f"通用課程資料遷移工具 - 課程{course_number}")
    print("=" * 50)
    
    # 可以在這裡修改資料庫連接參數
    migrator = UniversalCourseMigrator(
        host='localhost',
        user='root',
        password='',  # 請修改為您的資料庫密碼
        database='goodin_learning_platform'
    )
    
    if migrator.migrate_course(course_number):
        print(f"\n✅ 課程{course_number}遷移成功完成！")
        print("\n📝 後續步驟：")
        print(f"1. 修改 course{course_number}_api.py 從資料庫讀取資料")
        print(f"2. 測試前端課程{course_number}頁面顯示")
        print("3. 驗證所有功能正常運作")
    else:
        print(f"\n❌ 課程{course_number}遷移失敗，請檢查錯誤訊息並修正後重試")
        sys.exit(1)

if __name__ == "__main__":
    main()
