from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine, text
import json

# 假設已經有 SQLAlchemy engine
engine = create_engine('mysql+pymysql://user:password@localhost/dbname')

course_api = Blueprint('course_api', __name__)

@course_api.route('/api/course_content/<course_id>')
def get_course_content(course_id):
    # 讀取所有該課程的頁面
    sql = text("SELECT page_index, html_content, chart_type, chart_config, multi_steps FROM course_pages WHERE course_id = :cid ORDER BY page_index")
    with engine.connect() as conn:
        result = conn.execute(sql, cid=course_id)
        pages = []
        for row in result:
            # multi_steps 欄位轉回 list
            multi_steps = json.loads(row.multi_steps) if row.multi_steps else []
            pages.append({
                "page_index": row.page_index,
                "html_content": row.html_content,
                "chart_type": row.chart_type,
                "chart_config": row.chart_config,
                "multi_steps": multi_steps
            })
    return jsonify({"pages": pages})
