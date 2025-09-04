from models.db import get_db_connection
import re

class StockFilterModel:
    def __init__(self):
        # 財務指標對應的資料庫欄位
        self.field_mapping = {
            'EPS': 'eps',
            'ROE': 'roe', 
            'FCF': 'fcf',
            'DBR': 'debt_ratio',  # 負債比
            'YR': 'dividend_yield',  # 殖利率
            'YoY': 'revenue_growth'  # 營收成長率
        }
    
    def parse_condition(self, condition_str):
        """
        解析條件字串，將其轉換為 SQL WHERE 條件
        例如: "EPS > 10 且 ROE > 10 且 FCF > 0 且 DBR < 50"
        轉換為: "eps > 10 AND roe > 10 AND fcf > 0 AND debt_ratio < 50"
        """
        # 替換中文連接詞
        condition_str = condition_str.replace('且', ' AND ')
        condition_str = condition_str.replace('或', ' OR ')
        condition_str = condition_str.replace('介於', 'BETWEEN')
        
        # 處理範圍條件，例如: "EPS 介於 0~5"
        range_pattern = r'(\w+)\s+BETWEEN\s+(\d+(?:\.\d+)?)~(\d+(?:\.\d+)?)'
        def replace_range(match):
            field = match.group(1)
            min_val = match.group(2)
            max_val = match.group(3)
            db_field = self.field_mapping.get(field, field.lower())
            return f"{db_field} BETWEEN {min_val} AND {max_val}"
        
        condition_str = re.sub(range_pattern, replace_range, condition_str)
        
        # 替換財務指標為資料庫欄位名
        for indicator, db_field in self.field_mapping.items():
            # 使用正則表達式確保只替換完整的單詞
            pattern = r'\b' + re.escape(indicator) + r'\b'
            condition_str = re.sub(pattern, db_field, condition_str)
        
        return condition_str
    
    def filter_stocks_by_conditions(self, conditions):
        """
        根據多個條件篩選股票
        conditions: 條件列表，每個條件包含 tag, explanation, condition
        """
        conn = get_db_connection()
        if not conn:
            return {"error": "DB connection failed"}
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 建構 WHERE 條件
            where_conditions = []
            for cond in conditions:
                sql_condition = self.parse_condition(cond['condition'])
                if sql_condition.strip():
                    where_conditions.append(f"({sql_condition})")
            
            if not where_conditions:
                # 如果沒有條件，返回所有股票
                query = """
                    SELECT stock_code, stock_name, year_month, quarter, 
                           eps, roe, fcf, debt_ratio, dividend_yield, revenue_growth
                    FROM financial_data 
                    ORDER BY stock_code, year_month DESC, quarter DESC
                """
            else:
                # 合併所有條件，使用 AND 連接（股票必須符合所有選中的標籤條件）
                where_clause = " AND ".join(where_conditions)
                query = f"""
                    SELECT stock_code, stock_name, year_month, quarter,
                           eps, roe, fcf, debt_ratio, dividend_yield, revenue_growth
                    FROM financial_data 
                    WHERE {where_clause}
                    ORDER BY stock_code, year_month DESC, quarter DESC
                """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            # 按股票代號分組，只保留最新的財務數據
            stock_dict = {}
            for row in results:
                stock_code = row['stock_code']
                if stock_code not in stock_dict:
                    stock_dict[stock_code] = row
            
            return list(stock_dict.values())
            
        except Exception as e:
            return {"error": f"Database query failed: {str(e)}"}
        finally:
            conn.close()
    
    def get_tag_definitions(self):
        """
        返回所有標籤定義
        """
        return {
            "高成長平穩型": {
                "explanation": "公司長期獲利穩定，財務體質健康，適合長期投資。",
                "condition": "EPS > 10 且 ROE > 10 且 FCF > 0 且 DBR < 50"
            },
            "高成長型": {
                "explanation": "公司近期營收高速成長，代表進入快速擴張階段。",
                "condition": "YoY > 20"
            },
            "配息型": {
                "explanation": "現金殖利率高且穩定獲利，適合追求被動收入者。",
                "condition": "YR >= 5 且 EPS > 0"
            },
            "風險型": {
                "explanation": "公司虧損、負債高或現金流不穩，投資風險較大。",
                "condition": "EPS < 0 或 DBR > 70 或 FCF < 0"
            },
            "翻身型": {
                "explanation": "由虧轉盈，營運狀況開始改善，具轉機潛力。",
                "condition": "EPS 介於 0~5 且 YoY 介於 5~15"
            },
            "平穩型": {
                "explanation": "基本面穩定但缺乏成長動能，變化不大。",
                "condition": "EPS 介於 0~10 且 ROE 介於 5~15 且 YR 介於 0~5"
            },
            "話題型": {
                "explanation": "題材熱、人氣高但基本面尚未跟上，潛在波動大。",
                "condition": "YR < 1 且 YoY > 15"
            }
        }
    
    def test_condition_parsing(self, condition_str):
        """
        測試條件解析功能
        """
        return self.parse_condition(condition_str)
