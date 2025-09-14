from flask import Blueprint, jsonify
import pymysql
import json

course6_api = Blueprint('course6_api', __name__)

# 課程6資料（布林通道）
# course6_pages = [
#     {
#         "page_index": 0,
#         "html_content": """
#         <div class="m-4 font-large align-self-center">
#           <h1 class="fw-bolder mb-4 mt-2" style="">布林通道是什麼？</h1>
#           <p class="fs-5 mb-2">布林通道（Bollinger Bands）是技術分析大師 John Bollinger 發明的「波動率指標」。</p>
#         </div>
#         <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
#           <iframe src="https://giphy.com/embed/VbnUQpnihPSIgIXuZv" width="384" height="480" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/computer-cat-wearing-glasses-VbnUQpnihPSIgIXuZv">via GIPHY</a></p>
#         </div>
#         <div class="d-flex justify-content-center mb-5 pr-5">
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "multi_steps": []
#     },
#     {
#         "page_index": 1,
#         "html_content": """
#         <div class="m-4 font-large align-self-center">
#           <h1 class="fw-bolder mb-4 mt-2">布林通道是什麼？</h1>
#           <p class="fs-5 mb-2">在一條移動平均線（通常是 20 日均線）上下，畫出上軌和下軌，形成「通道」。</p>
#           <p class="fs-5 mb-2">觀察股價在通道中的位置，可以判斷是否「過熱」或「超賣」，以及市場波動狀況。</p>
#         </div>
#         <div id="chart-container" class="card shadow mb-4" style="display:flex;">
#           <div class="card-body align-self-center">
#             <div class="chart-area">
#               <canvas id="chart1" style="display: block; height: 320px;"></canvas>
#             </div>
#           </div>
#           <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解布林通道的變化喔～</p>
#         </div>
#         <div class="d-flex justify-content-center mb-5" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": "chart1",
#         "multi_steps": []
#     },
#     {
#         "page_index": 2,
#         "html_content": """
#         <div class="m-4 font-large align-self-center">
#           <h1 class="fw-bolder mb-4 mt-2 pl-4">為什麼要用布林通道？</h1>
#           <ul class="fs-5 mb-4" style="list-style-type: none;">
#             <li>它會隨波動自動調整寬度，能快速感知市場「熱度」。</li>
#             <ul>
#               <li>通道變寬 → 市場激烈</li>
#               <li>通道變窄 → 市場整理、盤整。</li>
#             </ul>
#           </ul>
#           <img  src="https://storage.googleapis.com/oanda-prod-asne1-oj-tw-wordpress/2021/07/21006.png" alt="cross types" style="max-width:80vw;">  
#           <p class="mt-4 w-75 text-muted medium" style="text-align:right;">
#             圖片來源：<a href="https://www.oanda.com/bvi-ft/lab-education/technical_analysis/use_bollinger_band/" target="_blank">
#                 善用布林通道掌握交易趨勢方向
#             </a>
#           </p> 
#           <p class="fs-5 mb-4 text-center"><strong>✨ 重點：布林通道是你的「波動雷達」。</strong></p>
#         </div>

#         <div class="d-flex justify-content-center mb-5" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "multi_steps": []
#     },
#     {
#         "page_index": 3,
#         "html_content": """
#         <div class="m-4 font-large align-self-center">
#           <h1 class="fw-bolder mb-4 mt-2">結構介紹（上軌、中軌、下軌）</h1>
#           <p class="fs-5 mb-2">中軌：20 日均線，代表短期平均水平。</p>
#           <p class="fs-5 mb-2">上軌：中軌 + 2 倍標準差，股價若突破，可能「過熱」或「強勢突破」。</p>
#           <p class="fs-5 mb-2">下軌：中軌 − 2 倍標準差，股價若跌破代表「超賣」或「弱勢」。</p>
#         </div>
#         <div id="chart-container" class="card shadow mb-4" style="display:flex;">
#           <div class="card-body align-self-center">
#             <div class="chart-area">
#               <canvas id="chart2" style="display: block; height: 320px;"></canvas>
#             </div>
#           </div>
#           <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解布林通道的變化喔～</p>
#         </div>
#         <div class="d-flex justify-content-center mb-5" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": "chart2",
#         "multi_steps": []
#     },
#     {
#         "page_index": 4,
#         "html_content": """
#         <div class="d-flex flex-column m-4 font-large align-self-center w-100" style="max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;">
#           <h1 class="fw-bolder mb-4 mt-2">生活化理解 — 彈簧 & 夜市</h1>
#           <p class="fs-5 mb-4">彈簧：</p>
#           <ul class="fs-5 mb-4">
#             <li>壓縮 → 收斂</li>
#             <li>放開 → 爆發。</li>
#           </ul>
#           <p class="fs-5 mb-4">夜市：</p>
#           <ul class="fs-5 mb-4">
#             <li>人多擠一起 → 通道窄，準備爆發</li>
#             <li>人散開 → 通道寬，行情冷清</li>
#           </ul>
#           <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
#             <iframe src="https://giphy.com/embed/f6v1HAqfj2svgGAqh9" width="480" height="293" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/usagi-chiikawa-hachiware-f6v1HAqfj2svgGAqh9">via GIPHY</a></p>
#           </div>
#         </div>
#         <div class="d-flex justify-content-center mb-5" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "multi_steps": []
#     },
#     {
#         "page_index": 5,
#         "html_content": """
#         <div class="m-4 font-large" style="align-self: center;">
#           <h2 class="fw-bolder mb-4 mt-2">觀察重點 — 收斂與擴張</h2>
#           <ul class="fs-5 mb-4">
#             <li>收斂：進入整理期，是大行情的前兆。</li>
#             <li>擴張：行情劇烈，若有趨勢，可能持續一段時間。</li>
#           </ul>
#           <img  src="https://storage.googleapis.com/image.gugu.fund/169052163251939647830985.png" alt="cross types" style="max-width:50vw;">  
#           <p class="mt-4 text-muted medium" style="text-align:center;">
#             圖片來源：<a href="https://school.gugu.fund/blog/trade-skill/3207451284" target="_blank">
#                 布林通道是什麼？布林通道找出買賣點，布林通道設定教學 -技術分析
#             </a>
#           </p> 
#         </div>

#         <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "multi_steps": []
#     },
#     {
#         "page_index": 6,
#         "html_content": """
#         <div class="m-4 font-large" style="align-self: center;">
#           <h2 class="fw-bolder mb-4 mt-2">觀察重點 — 收斂與擴張</h2>
#           <ul class="fs-5 mb-4">
#             <li>上軌（壓力帶）：靠近時注意回檔壓力；但若帶量突破，代表多頭強勢。</li>
#             <li>下軌（支撐帶）：靠近時有機會反彈；若帶量跌破，要小心續跌。</li>
#           </ul>
#         </div>
#         <div id="carousel" class="d-flex flex-column align-items-center w-75 mb-4" style="align-self: center; display: none;"></div>

#         <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "multi_steps": ["carousel"],
#         "carousel_items": [
#             {
#                 "src": "https://storage.googleapis.com/image.gugu.fund/169052160872870785382355.png",
#                 "alt": "股價突破上軌",
#                 "caption": "股價突破上軌後布林通道打開",
#                 "credit": "圖片來源：<a href=\"https://school.gugu.fund/blog/trade-skill/3207451284\" target=\"_blank\">布林通道是什麼？布林通道找出買賣點，布林通道設定教學 -技術分析</a>"
#             },
#             {
#                 "src": "https://storage.googleapis.com/image.gugu.fund/169052166356480408607304.png",
#                 "alt": "股價跌破下軌",
#                 "caption": "股價跌破下軌後布林通道打開",
#                 "credit": "圖片來源：<a href=\"https://school.gugu.fund/blog/trade-skill/3207451284\" target=\"_blank\">布林通道是什麼？布林通道找出買賣點，布林通道設定教學 -技術分析</a>"
#             }
#         ]
#     },
#     {
#         "page_index": 7,
#         "html_content": """
#         <div class="m-4 font-large" style="align-self: center;">
#           <h2 class="fw-bolder mb-4 mt-2">實戰應用 — 台股情境</h2>
#           <p class="fs-5 mb-2">觀察台股：</p>
#           <ul class="fs-5 mb-4">
#             <li>通道收窄、量縮 → 觀望。</li>
#             <li>突然長紅 K 並放量突破上軌 → 多頭可能起漲，可考慮分批進場並設停損。</li>
#             <li>若長綠 K 跌破下軌 → 空頭來襲，須考慮減碼或停損。</li>
#           </ul>
#         </div>
#         <div id="carousel" class="d-flex flex-column align-items-center w-75 mb-4" style="align-self: center; display: none;"></div>

#         <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "multi_steps": ["carousel"],
#         "carousel_items": [
#             {
#                 "src": "https://storage.googleapis.com/image.gugu.fund/169052169541473428765384.png",
#                 "alt": "技術面上軌突破",
#                 "caption": "股價突破上軌後布林通道打開 ",
#                 "credit": "圖片來源：<a href=\"https://school.gugu.fund/blog/trade-skill/3207451284\" target=\"_blank\">布林通道是什麼？布林通道找出買賣點，布林通道設定教學 -技術分析</a>"
#             },
#             {
#                 "src": "https://storage.googleapis.com/image.gugu.fund/169052162104218069101028.png",
#                 "alt": "股價跌破下軌",
#                 "caption": "技術面突破反轉月K線",
#                 "credit": "圖片來源：<a href=\"https://school.gugu.fund/blog/trade-skill/3207451284\" target=\"_blank\">布林通道是什麼？布林通道找出買賣點，布林通道設定教學 -技術分析</a>"
#             }
#         ]
#     },
#     {
#         "page_index": 8,
#         "html_content": """
#         <div class="m-4 font-large align-self-center">
#           <h1 class="fw-bolder mb-4 mt-2 pl-3" style="">風險控管 & 心法</h1>
#           <p class="fs-5 mb-2">不要只靠布林通道，還要參考 K 線、均線、成交量等。</p>
#           <p class="fs-5 mb-2">停損、停利要設定，並保持分批進出，避免 all in。</p>
#           <p class="fs-5 mb-2">正確心態：學習 & 驗證，不把它當魔法水晶球。</p>
#         </div>
#         <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
#           <iframe src="https://giphy.com/embed/cLLgfNJiKppgA" width="480" height="480" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/money-cLLgfNJiKppgA">via GIPHY</a></p>
#         </div>
#         <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "multi_steps": []
#     },
#     {
#         "page_index": 9,
#         "html_content": """
#         <div class="m-4 font-large align-self-center">
#           <h1 class="fw-bolder mb-4 mt-2" style="">結語 — 先學會，再熟練</h1>
#           <p class="fs-5 mb-2">建議先熟悉基本技術指標（如均線、K 線、成交量）。</p>
#           <p class="fs-5 mb-2">多模擬、小額測試，累積經驗後再加碼。</p>
#           <p class="fs-5 mb-2">結合總體經濟、大盤趨勢、籌碼面，全面判斷。</p>
#           <p class="fs-5 mb-2">布林通道不是魔法球，而是幫助你讀懂「市場呼吸」的工具！</p>
#         </div>
#         <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
#           <iframe src="https://giphy.com/embed/tHIRLHtNwxpjIFqPdV" width="480" height="480" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/justin-raccoon-pedro-tHIRLHtNwxpjIFqPdV">via GIPHY</a></p>
#         </div>
#         <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
#           <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
#             <span class="text">回上一頁</span>
#           </a>
#           <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
#             <span class="text">前往課後練習</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "multi_steps": []
#     }
# ]

@course6_api.route('/api/course_content/course6')
def get_course6_content():
    conn = pymysql.connect(
        host='140.127.220.85',
        user='nukim',
        password='nukim',
        database='goodin',
        charset='utf8mb4'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT page_index, html_content, chart_type, chart_config, multi_steps, carousel_items "
        "FROM course_pages WHERE course_id=%s ORDER BY page_index", ('course6',)
    )
    rows = cursor.fetchall()
    # 轉換 JSON 欄位
    for row in rows:
        if row['multi_steps']:
            row['multi_steps'] = json.loads(row['multi_steps'])
        if row['carousel_items']:
            row['carousel_items'] = json.loads(row['carousel_items'])
    cursor.close()
    conn.close()
    return jsonify({'pages': rows})
