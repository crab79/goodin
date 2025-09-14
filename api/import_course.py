import pymysql
import json

# 假設你已經有 course9_pages 這個 list
from course9_api import course9_pages

conn = pymysql.connect(
    host='140.127.220.85',
    user='nukim',
    password='nukim',
    database='goodin',
    charset='utf8mb4'
)
cursor = conn.cursor()

for page in course9_pages:
    sql = """
    INSERT INTO course_pages
    (course_id, page_index, html_content, chart_type, chart_config, multi_steps, carousel_items)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        'course9',
        page['page_index'],
        page['html_content'],
        page.get('chart_type'),
        page.get('chart_config'),
        json.dumps(page.get('multi_steps')) if page.get('multi_steps') else None,
        json.dumps(page.get('carousel_items')) if page.get('carousel_items') else None,
    ))

conn.commit()
cursor.close()
conn.close()