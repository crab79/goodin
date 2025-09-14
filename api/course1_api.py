from flask import Blueprint, jsonify
import pymysql
import json

course1_api = Blueprint('course1_api', __name__)

# 課程1資料（可直接編輯，日後可改為資料庫讀取）
# course1_pages = [
#     {
#         "page_index": 0,
#         "html_content": """
#         <div class=\"m-4 font-large align-self-center\">
#           <h1 class=\"fw-bolder mb-4 mt-2\">🎉 歡迎來到GOODIN系列課程！ 🎉</h1>
#           <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">我們將學習的內容包括： 
#             <li>✅ 價格趨勢判斷（就像看路線圖，判斷市場是上坡還是下坡）</li>
#             <li>✅ 市場動能分析（像觀察車流，了解市場買賣力道是否強勁）</li>
#             <li>✅ 技術指標應用（像是車上的導航系統，幫助你判斷轉彎點）</li>
#           </ul>
#         </div>
#         <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#           <span class=\"text\">繼續</span>
#         </a>
#         <p class=\"text-muted medium\" style=\"text-align:center;margin-top:20%;\">⚠️ 溫馨提醒：投資市場就像開車上路，除了學習導航與技術分析，還需要控制風險，避免發生意外！</p>
#         """,
#         "chart_type": None,
#         "chart_config": None
#     },
#     {
#         "page_index": 1,
#         "html_content": """
#         <div class=\"m-4 font-large align-self-center\">
#           <h1 class=\"fw-bolder mb-4 mt-2\">GOODIN課程將涵蓋以下主題</h1>
#           <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">
#             <li>📌第一課：課程介紹 + 技術分析基礎概念（本堂）</li>
#             <li>📌第二課：K 線圖初探（學習「市場的心電圖」）</li>
#             <li>📌第三課：移動平均線 SMA（就像投資的方向指標）</li>
#             <li>📌第四課：相對強弱指標 RSI（評估市場的「體力」）</li>
#             <li>📌第五課：相對強弱指數 RSI 進階篇（解讀「市場體力」的細節）</li>
#             <li>📌第六課：布林通道 + 常見型態（看見「價格的彈性空間」）</li>
#             <li>📌第七課：MACD 指標（觀察趨勢與動能的「雙重節奏」）</li>
#             <li>📌第八課：KD 隨機指標（發現市場的「節奏感」）</li>
#             <li>📌第九課：乖離率 BIAS（判斷價格偏離程度的「溫度計」）</li>
#           </ul>
#         </div>
#         <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#           <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#             <span class=\"text\">回上一頁</span>
#           </a>
#           <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#             <span class=\"text\">繼續</span>
#           </a>
#         </div>
#         """,
#         "chart_type": None,
#         "chart_config": None
#     },
#       {
#           "page_index": 2,
#           "html_content": """
#           <div class=\"m-4 font-large\" style=\"align-self: center;\">
#             <h2 class=\"fw-bolder mb-4 mt-2\">何謂「技術分析」？</h2>
#             <p class=\"fs-5 mb-4\">💡核心概念-技術分析就像是「氣象預報」。</p>
#             <ul class=\"fs-5 mb-4\"> 透過以下因素來推測未來市場的走勢。：
#               <li>「氣溫變化」（價格）</li>
#               <li>「風速」（成交量）</li>
#               <li>「天氣型態」（技術指標）</li>
#             </ul>
#             <div id=\"text-container\" class=\"m-4 font-large flex-column\" style=\"align-self: center;display:none;\">
#               <p class=\"fs-5 mb-4\">不論是公司財報、經濟數據、投資人情緒，這些因素最終都會反映在價格波動中。因此，技術分析不關心「為什麼下雨」，而是專注於「天氣預報」，以判斷該不該帶雨傘（買賣時機）。</p>
#               <div class=\"d-flex flex-column align-items-center\" style=\"align-self: center;\">
#                 <iframe src=\"https://giphy.com/embed/StlcqIUSbiLHYt7X5U\" width=\"480\" height=\"271\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/ikonpass-powder-day-ikon-pass-weather-channel-StlcqIUSbiLHYt7X5U\">via GIPHY</a></p>
#               </div>
#             </div>
#           <p id=\"text\" class=\"fs-5 mb-4\" style=\"display:none;\">換句話說，技術分析是一種單純根據商品「價格」和「成交量」，並透過圖像、數據和指標的輔助，對金融市場的未來走勢進行預判和做出交易策略。</p>
#           </div>
#           <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#               <span class=\"text\">回上一頁</span>
#             </a>
#             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#               <span class=\"text\">繼續</span>
#             </a>
#           </div>
#           <p class=\"mt-4 text-muted medium\" style=\"text-align:center;\">
#           參考資料：<a href=\"https://quantpass.org/technical-analysis-lists/\" target=_blank>
#               技術分析教學懶人包，K線圖、K棒型態學、技術指標一次搞懂
#           </a>
#           </p> 
#           """,
#           "chart_type": None,
#           "chart_config": None,
#           "multi_steps": ["text-container", "text"]
#       },
#       {
#           "page_index": 3,
#           "html_content": """
#           <div class=\"m-4 font-large\" style=\"align-self: center;\">
#             <h2 class=\"fw-bolder mb-4 mt-2\">技術分析 vs 基本面分析</h2>
#             <p class=\"fs-5 mb-4\">📊 技術分析 vs. 基本面分析</p>
#             <ul class=\"fs-5 mb-4\">
#               <li>基本面分析：像是你正在選擇要前去用餐的餐廳，會研究店家評價（公司財報）、菜色品質（產品競爭力）、客流量（市場需求）來決定是否過去用餐。</li>
#               <li>技術分析：則像是觀察排隊人數（價格趨勢）、餐廳氣氛（市場情緒）和食物賣完的速度（成交量），來判斷是否值得跟風。</li>
#             </ul>      
#           </div>
#           <div class=\"card-body\">
#             <div class=\"table-responsive\">
#               <table class=\"table table-bordered\">
#                 <thead>
#                   <tr>
#                     <th> </th>
#                     <th>基本分析</th>
#                     <th>技術分析</th>
#                   </tr>
#                 </thead>
#                 <tbody>
#                   <tr>
#                     <td><strong>關注項目</strong></td>
#                     <td>企業價值、財報</td>
#                     <td>商品價格、商品成交數量</td>
#                   </tr>
#                   <tr>
#                     <td><strong>資料來源</strong></td>
#                     <td>公司財報、新聞</td>
#                     <td>K線、技術指標</td>
#                   </tr>
#                   <tr>
#                     <td><strong>用途</strong></td>
#                     <td>長期投資判斷</td>
#                     <td>抓波段操作點</td>
#                   </tr>
#                 </tbody>
#               </table>
#               </div>
#           </div>
#           <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#               <span class=\"text\">回上一頁</span>
#             </a>
#             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#               <span class=\"text\">繼續</span>
#             </a>
#           </div>
#           """,
#           "chart_type": None,
#           "chart_config": None
#       },
#       {
#           "page_index": 4,
#           "html_content": """
#           <div class=\"m-4 font-large\" style=\"align-self: center;\">
#             <h2 class=\"fw-bolder mb-4 mt-2\">為何要學習技術分析？</h2>
#             <p class=\"fs-5 mb-4\">✅ 快速判斷市場氛圍：</p>
#             <p class=\"fs-5 mb-4\">看到 K 線翻黑，就像天氣突然轉陰，可能要準備雨具（制定停損策略）。
#             當技術指標翻轉，就像體感溫度驟降，可能是市場轉冷(市場的買氣及熱度正在減弱)的訊號。</p>
#             <p class=\"fs-5 mb-4\">✅ 掌握買賣時機：</p>
#             <p class=\"fs-5 mb-4\">透過支撐壓力位（市場的「停車位」）、乖離率（市場的「車速表」）來決定入場(買進點)或出場(賣出點)的最佳時間。</p>
#             <p class=\"fs-5 mb-4\">✅ 風險控管：</p>
#             <p class=\"fs-5 mb-4\">設定停損點，當市場出現意外波動時，能夠降低損失。</p>
#           </div>
#           <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#               <span class=\"text\">回上一頁</span>
#             </a>
#             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#               <span class=\"text\">繼續</span>
#             </a>
#           </div>
#           """,
#           "chart_type": None,
#           "chart_config": None
#       },
#       {
#           "page_index": 5,
#           "html_content": """
#           <div class=\"m-4 font-large\" style=\"align-self: center;\">
#             <h2 class=\"fw-bolder mb-4 mt-2\">技術分析三大觀察面向</h2>
#             <p class=\"fs-5 mb-4\">🟢 價格 Price｜就像車子的「時速表」</p>
#             <ul class=\"fs-5 mb-4\">
#               <li>觀察工具：K 線圖、價格型態</li>
#               <li>作用說明：如果價格一路往上，表示市場有「衝勁」；若突然急轉或停滯，可能表示有些微風險。</li>
#             </ul> 
#             <div id=\"text2\" class=\"flex-column\" style=\"display:none;\">
#               <p class=\"fs-5 mb-4\">🔵 技術指標 Indicators｜就像車子的「監控系統」</p>
#               <div class=\"table-responsive\">
#                 <table class=\"table table-bordered\">
#                   <thead>
#                     <tr>
#                       <th>指標</th>
#                       <th>作用</th>
#                       <th>比喻</th>
#                     </tr>
#                   </thead>
#                   <tbody>
#                     <tr>
#                       <td>SMA移動平均線</td>
#                       <td>趨勢判斷</td>
#                       <td>導航：告訴你該往哪邊走</td>
#                     </tr>
#                     <tr>
#                       <td>RSI相對強弱指標</td>
#                       <td>市場是否過熱/過冷</td>
#                       <td>油箱：看市場是否太累了</td>
#                     </tr>
#                     <tr>
#                       <td>KD 指標</td>
#                       <td>超買超賣</td>
#                       <td>溫度計:過熱小心中暑(漲過頭)</td>
#                     </tr>
#                     <tr>
#                       <td>MACD</td>
#                       <td>動能變化</td>
#                       <td>雷達:偵測轉強或轉弱的訊號</td>
#                     </tr>
#                     <tr>
#                       <td>乖離率</td>
#                       <td>偏離程度</td>
#                       <td>加速感測器:跑太快可能要回調</td>
#                     </tr>
#                   </tbody>
#                 </table>
#               </div>
#             </div>
#             <div id=\"text3\" class=\"flex-column\" style=\"display:none;\">
#               <p class=\"fs-5 mb-4\">🟠 成交量 Volume｜就像車子的「油門」</p>
#               <ul class=\"fs-5 mb-4\">
#                 <li>觀察工具：量能圖、成交量均線</li>
#                 <li>作用說明：成交量代表市場參與的熱度，是驅動價格的力量，就像「油門」。</li>
#                 <li>如果價格上漲但成交量縮小，表示「車子在加速，卻沒踩油門」➡ 可能是虛假行情。</li>
#                 <li>沒油的加速，是衝不遠的！（價漲量縮＝虛假行情）</li>
#               </ul> 
#             </div>
#           </div>
#           <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
#             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#               <span class=\"text\">回上一頁</span>
#             </a>
#             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#               <span class=\"text\">繼續</span>
#             </a>
#           </div>
#           """,
#           "chart_type": None,
#           "chart_config": None,
#           "multi_steps": ["text2", "text3"]
#       },
#       {
#           "page_index": 6,
#           "html_content": """
#           <div class=\"d-flex flex-column m-4 font-large\" style=\"align-self: center;\">
#             <h2 class=\"fw-bolder mb-4 mt-2\">常見的技術分析方法</h2>
#             <p class=\"fs-5 mb-4\">📍 趨勢判斷</p>
#             <ul class=\"fs-5 mb-4\">
#               <li>移動平均線（SMA）就像是「方向指示牌」，幫助判斷市場是往上（牛市）還是往下（熊市）。</li>
#             </ul> 
#             <div class=\"d-flex flex-column w-75 align-self-center align-items-center\">
#                 <img src=\"https://lh4.googleusercontent.com/GW6mNKgM4DAxAvNu_8kG8riVUSsQ52isjHsjJ1bKh5Mw3n-XmdwXfuLNfVtwHROdezZSZU1AoBFt3cfET4sC9E5jZxvg4lEp0CTM0hqtc8qHaHUMMFfE9r1aELixAY1DDopAMGRkJ_D7SEO2YW5lEGJwrTOeqslaKtMXdSeyNkicU7YOJn_y10S4Ug\" alt=\"stock market chart\" class=\"w-75\">
#                 <p class=\"mt-4 text-muted medium\">
#                 圖片來源：<a href=\"https://www.mitrade.com/zh/insights/forex/forex-education/what-is-simple-moving-average\" target=_blank>
#                     【簡單移動平均線（SMA）是什麼？如何利用SMA進行交易？
#                 </a>
#                 </p>
#             </div> 
#             <div id=\"text2\" class=\"flex flex-column\" style=\"display:none;\">
#               <p class=\"fs-5 mb-4\">📍 趨勢判斷</p>
#               <ul class=\"fs-5 mb-4\">
#                 <li>K 線圖與各種價格型態（如「雙峰山」= 可能回落、「U 型谷底」= 可能反彈）幫助預測市場動向。</li>
#               </ul>
#               <div class=\"d-flex flex-column w-75 align-self-center align-items-center\">
#                 <img src=\"https://support.fugle.tw/wp-content/uploads/2024/11/K%E7%B7%9A%E6%98%AF%E4%BB%80%E9%BA%BC-768x768.png\" alt=\"stock market chart\" class=\"w-50\">
#                 <p class=\"mt-4 text-muted medium\">
#                 圖片來源：<a href=\"https://support.fugle.tw/trading/trading-dictionary/15971/\" target=_blank>
#                     如何判讀 K 線？16 種 K 線型態一次了解
#                 </a>
#                 </p> 
#               </div>
#             </div>
#             <div id=\"text3\" class=\"flex-column\" style=\"display:none;\">
#               <p class=\"fs-5 mb-4\">📍 震盪指標（Oscillator）</p>
#               <ul class=\"fs-5 mb-4\">
#                 <li>RSI、KD、乖離率等指標，就像是「測速雷達」，當市場超買或超賣時，可能即將進入轉折點。</li>
#               </ul> 
#             </div>
#           </div>
#           <div class=\"d-flex justify-content-center mb-4\" style=\"gap: 10%\">
#             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#               <span class=\"text\">回上一頁</span>
#             </a>
#             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#               <span class=\"text\">繼續</span>
#             </a>
#           </div>
#           """,
#           "chart_type": None,
#           "chart_config": None,
#           "multi_steps": ["text2", "text3"]
#       },
#       {
#           "page_index": 7,
#           "html_content": """
#           <div class=\"m-4 font-large\" style=\"align-self: center;\">
#             <h2 class=\"fw-bolder mb-4 mt-2\">如何搭配使用？</h2>
#             <p class=\"fs-5 mb-4\">🔄 多重指標驗證</p>
#             <ul class=\"fs-5 mb-4\">
#               <li>單一指標不可靠，就像開車時不能只看車速表，還要觀察路況、導航與油量。</li>
#               <li>乖離率過大但 RSI 顯示正常？可能市場還沒過熱，不要太早進場。</li>
#             </ul> 
#             <p class=\"fs-5 mb-4\">📆 細分交易週期</p>
#             <ul class=\"fs-5 mb-4\">
#               <li>短線交易（像跑一百公尺）：重視 RSI、乖離率、KD 等震盪指標。</li>
#               <li>長線交易（像跑馬拉松）：關注 SMA、趨勢線、型態學掌握大方向。</li>
#             </ul> 
#           </div>
#           <div class=\"d-flex flex-column align-items-center w-75\" style=\"align-self: center;\">
#             <iframe src=\"https://giphy.com/embed/sRKg9r2YWeCTG5JTTo\" width=\"480\" height=\"480\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/running-run-runs-sRKg9r2YWeCTG5JTTo\">via GIPHY</a></p>
#           </div>
#           <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#               <span class=\"text\">回上一頁</span>
#             </a>
#             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#               <span class=\"text\">繼續</span>
#             </a>
#           </div>
#           """,
#           "chart_type": None,
#           "chart_config": None
#       },
#       {
#           "page_index": 8,
#           "html_content": """
#           <div class=\"m-4 font-large\" style=\"align-self: center;\">
#             <h2 class=\"fw-bolder mb-4 mt-2\">第一課總結</h2>
#             <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">
#               <li>🔹 技術分析 = 投資導航系統，幫助你避開危險區，找到最佳進場點。</li>
#               <li>🔹 市場三大支柱：價格、成交量、技術指標，共同決定市場方向。 </li>
#               <li>🔹 趨勢分析 vs. 震盪分析，搭配不同指標來預測市場變動。</li>
#             </ul>
#           </div>
#           <div class=\"d-flex flex-column align-items-center w-75\" style=\"align-self: center;\">
#               <iframe src=\"https://giphy.com/embed/bMycGOQLESDCEnLNUz\" width=\"480\" height=\"360\" style=\"align-self: center;\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/moodman-reaction-bMycGOQLESDCEnLNUz\">via GIPHY</a></p> 
#           </div>
#           <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#               <span class=\"text\">回上一頁</span>
#             </a>
#             <a href=\"#\" class=\"btn btn-info btn-icon-split align-self-center\" id=\"continue-btn\">
#               <span class=\"text\">前往課後練習</span>
#             </a>
#           </div>
#           <p class=\"fs-5 mb-4 mt-5\" style=\"text-align:center\">📌 下一課：K 線圖初探 🧐 將帶你深入了解 K 線的結構與多空力道，讓你能讀懂市場的「心電圖」！</p>
#           """,
#           "chart_type": None,
#           "chart_config": None
#       }
# ]

@course1_api.route('/api/course_content/course1')
def get_course1_content():
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
        "FROM course_pages WHERE course_id=%s ORDER BY page_index", ('course1',)
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
