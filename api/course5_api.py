from flask import Blueprint, jsonify

course5_api = Blueprint('course5_api', __name__)

# 課程5資料（可直接編輯，日後可改為資料庫讀取）
course5_pages = [
        {
                "page_index": 0,
                "html_content": """
                <div class="m-4 font-large align-self-center">
                    <h1 class="fw-bolder mb-4 mt-2 pl-3" style="">相對強弱指標  RSI（Relative Strength Index)</h1>
                    <ul class="fs-5 mb-4">
                        <li>一種技術分析指標，用以衡量市場價格<strong>在「一段時間內」上漲與下跌的強度</strong><br>幫助投資者判斷市場<strong>是否處於「超買」或「超賣」狀態</strong></li>
                        <li>可以在技術分析中，透過數值變化提供市場動能的衡量標準<br>幫助投資者識別潛在的買入與賣出時機。</li>
                    </ul>
                </div>
                <div id="chart-container" class="card shadow mb-4" style="display:flex;">
                    <div class="card-body align-self-center">
                        <div class="chart-area">
                            <canvas id="chart1" style="display: block; height: 320px;"></canvas>
                        </div>
                    </div>
                    <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解RSI的變化喔～</p>
                </div>
                <div class="d-flex justify-content-center mb-5 pr-5">
                    <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                        <span class="text">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": "chart1",
                "chart_config": None
        },
        {
                "page_index": 1,
                "html_content": """
                <div class="m-4 font-large align-self-center">
                    <h1 class="fw-bolder mb-4 mt-2">RSI的用途</h1>
                    <p class="fs-5 mb-2">一、觀察數值</p>
                    <p class="fs-5 mb-2">📌 台股常用設定為：14日 RSI</p>
                    <div class="table-responsive mb-4">
                        <table class="table table-bordered">
                            <tbody>
                                <tr>
                                    <th style="text-align:middle;">RSI數值</th>
                                    <th style="text-align:middle;">狀態</th>
                                    <th style="text-align:middle;">解釋</th>
                                </tr>
                                <tr>
                                    <td>0~30</td>
                                    <td>超賣區</td>
                                    <td>下跌過頭，可能準備反彈(低接機會)</td>
                                </tr>
                                <tr>
                                    <td>31~70</td>
                                    <td>正常區</td>
                                    <td>市場健康波動，無明顯過熱或過冷</td>
                                </tr>
                                <tr>
                                    <td>71~100</td>
                                    <td>超買區</td>
                                    <td>上漲太多，可能短線過熱(高檔拉回風險)</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div id="text" class="flex-column" style="display:none">
                        <ul class="fs-5 mb-4" style="list-style-type: none;padding-left: 0;">
                            <li class="fs-5 mb-4">二、幫你避免「追高殺低」的衝動錯誤
                                <ul style="">
                                    <li>判斷超買或超賣</li>
                                </ul>
                            </li>
                            <li class="fs-5 mb-4">三、搭配其他指標使用(例如：K線、SMA)
                                <ul style="">
                                    <li>如果股價跌破支撐 + RSI < 30 → 趨勢仍弱</li>
                                    <li>若 RSI < 30 + 股價出現紅K → 反彈訊號</li>
                                </ul>
                            </li>
                            <li class="fs-5 mb-4">四、不受價格絕對高低影響
                                <ul style="">
                                    <li>RSI 看的是力道強弱，不是價格本身高低</li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="d-flex justify-content-center mb-5" style="gap: 10%">
                    <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
                        <span class="text">回上一頁</span>
                    </a>
                    <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                        <span class="text">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["text"]
        },
        {
                "page_index": 2,
                "html_content": """
                <div class="m-4 font-large align-self-center">
                    <h1 class="fw-bolder mb-4 mt-2 pl-4">相對強弱指數的概念</h1>
                    <ul class="fs-5 mb-4" style="list-style-type: none;">
                        <li>🧠 用日常生活來理解—電池電量 🔋⚡</li>
                        <li>當電量快沒了（接近 0%）時，你會趕快插上充電器（類似 超賣）</li>
                    </ul>
                    <ul style="list-style-type: none;">
                        <li>對應 RSI 概念：</li>
                        <ul>
                            <li>RSI > 70(超買)：電池快充滿了需要冷卻，市場可能也要休息一下（價格有機會回調）</li>
                            <li>RSI < 30(超賣)：電池快沒電了，需要充電，市場可能會反彈補足能量</li>
                        </ul>
                    </ul>
                    <p class="fs-5 mb-4 text-center"><strong>電池電量 → 市場過熱 or 過冷</strong></p>
                </div>
                <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
                    <iframe src="https://giphy.com/embed/AMqCTHuCMFpM4" width="480" height="264" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/adventure-time-tired-bmo-AMqCTHuCMFpM4">via GIPHY</a></p>
                </div>
                <div class="d-flex justify-content-center mb-5" style="gap: 10%">
                    <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
                        <span class="text">回上一頁</span>
                    </a>
                    <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                        <span class="text">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None
        },
        {
                "page_index": 3,
                "html_content": """
                <div class="m-4 font-large align-self-center">
                    <h1 class="fw-bolder mb-4 mt-2">計算公式與應用1</h1>
                    <p class="fs-5 mb-4">1️⃣ RSI 計算公式</p>
                    <p>RSI 的計算包含兩個主要部分：</p>
                    <p>RS (Relative Strength, 相對強度)</p>
                    $$RS = \\frac{\\text{平均上漲幅度}}{\\text{平均下跌幅度}}$$
                    <p>RSI (Relative Strength Index, 相對強弱指數)</p>
                    $$RSI = 100 - \\frac{100}{1 + RS}$$
                    <div id="text1"  style="display:none;">
                        <ul class="fs-5 mb-4">
                            <li>計算步驟解析：</li>
                                <ol class="fs-5 mb-4">
                                    <li>計算一段時間內（如：14天）的上漲、下跌價格變動。</li>
                                    <li>計算14天內的平均上漲與下跌的幅度。</li>
                                    <li>計算相對強弱（RS），即平均上漲幅度除以平均下跌幅度。</li>
                                    <li>套用RSI公式，得出RSI數值。</li>
                                </ol>
                        </ul>
                    </div>
                    <div id="text2"  style="display:none;">
                        <ul class="fs-5 mb-4">
                            <li>進一步簡化理解：<strong>最近這段時間內，股票漲、跌的力道誰比較強？</strong></li>
                                <ul class="fs-5 mb-4">
                                    <li>漲得多：RSI 上升</li>
                                    <li>跌得多：RSI 下降</li>
                                    <li>最後把這個強弱關係轉成一個 0 到 100 的數字</li>
                                </ul>
                        </ul>
                    </div>
                </div>
                <div class="d-flex justify-content-center mb-5" style="gap: 10%">
                        <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
                            <span class="text">回上一頁</span>
                        </a>
                        <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                            <span class="text">繼續</span>
                        </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["text1", "text2"]
        },
        {
                "page_index": 4,
                "html_content": """
                <div class="d-flex flex-column m-4 font-large align-self-center w-100" style="max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;">
                    <h1 class="fw-bolder mb-4 mt-2">計算公式與應用2</h1>
                    <p class="fs-5 mb-4">2️⃣ 可視化步驟法</p>
                    <p>範例：假設連續 14 天股價如下：</p>
                    <p>📈 上漲天數有 9 天，<strong>平均漲幅為 +2%</strong><br>📉下跌天數有 5 天，<strong>平均跌幅為 -1%</strong></p>
                    <ul class="fs-5 mb-4">
                        <li>步驟一：計算 RS（漲跌比）</li>
                            <ul class="fs-5 mb-4" style="list-style-type:none;">
                                <li>$$公式：RS = \\frac{\\text{平均上漲幅度}}{\\text{平均下跌幅度}}$$</li>
                                <li>$$RS = \\frac{2}{1} = 2$$</li>
                            </ul>
                    </ul>
                    <div id="text1"  style="display:none;">
                        <ul class="fs-5 mb-4">
                            <li>步驟二：代入 RSI 公式</li>
                                <ul class="fs-5 mb-4" style="list-style-type:none;">
                                    <li>$$公式：RSI = 100 - \\frac{100}{1 + RS}$$</li>
                                    <li>$$RSI = 100 - \\frac{100}{1 + 2} = 100 - \\frac{100}{3} = 100 - 33.33 = 66.67$$</li>
                                </ul>
                        </ul>
                    </div>
                    <div id="text2"  style="display:none;">
                        <p class="fs-5 mb-4"><strong>結論：RSI 約 67，市場偏強，但尚未超買。</strong></p>
                    </div>
                </div>
                <div class="d-flex justify-content-center mb-5" style="gap: 10%">
                    <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
                        <span class="text">回上一頁</span>
                    </a>
                    <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                        <span class="text">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["text1", "text2"]
        },
        {
                "page_index": 5,
                "html_content": """
                <div class="m-4 font-large" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">計算公式與應用3</h2>
                    <p class="fs-5 mb-4">3️⃣ RSI 的實用觀察法</p>
                    <ul class="fs-5 mb-4">
                        <li>RSI 在 50 附近 ➡️市場觀望，尚未明顯方向</li>
                        <li>RSI 突破 70 向上 ➡️強勢股，不是馬上賣，而是留意高檔轉弱訊號</li>
                        <li>RSI 跌破 30 向下 ➡️留意是否超賣反彈，但不代表馬上進場（需配合 K 線觀察）</li>
                    </ul>
                    <div id="text1" class="flex-column" style="display:none;">
                        <p class="fs-5 mb-4">4️⃣ 小提醒：常見誤區</p>
                        <div class="table-responsive mb-4">
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th class="text-center">常見誤區</th>
                                        <th class="text-center">正確觀念</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>❌ RSI &gt; 70 就一定要賣？</td>
                                        <td>✅ 有時是「強勢鈍化」，應觀察其他訊號。</td>
                                    </tr>
                                    <tr>
                                        <td>❌ RSI &lt; 30 就一定會反彈？</td>
                                        <td>✅ 可能是「跌勢加速」，要看有無止跌 K 線。</td>
                                    </tr>
                                    <tr>
                                        <td>❌ RSI 數值越高，漲勢越安全？</td>
                                        <td>✅ 高檔代表風險也變高，進場要謹慎。</td>
                                    </tr>
                                    <tr>
                                        <td>❌ RSI 可以單獨決定買賣時機？</td>
                                        <td>✅ 最佳做法是搭配 K 線、成交量、均線綜合判斷。</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
                    <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
                        <span class="text">回上一頁</span>
                    </a>
                    <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                        <span class="text">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["text1"]
        },
        {
                "page_index": 6,
                "html_content": """
                <div class="m-4 font-large" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">實際圖表展示</h2>
                </div>

                <div id="chart-container" class="card shadow mb-4" style="display:flex;">
                    <div class="card-body align-self-center">
                        <div class="chart-area">
                            <canvas id="chart2" style="display: block; height: 320px;"></canvas>
                        </div>
                    </div>
                    <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解RSI的變化喔～</p>
                </div>

                <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
                    <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
                        <span class="text">回上一頁</span>
                    </a>
                    <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                        <span class="text">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": "chart2",
                "chart_config": None
        },
        {
                "page_index": 7,
                "html_content": """
                <div class="m-4 font-large" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">實際圖表展示</h2>
                </div>

                <div id="chart-container" class="card shadow mb-4" style="display:flex;">
                    <div class="card-body align-self-center">
                        <div class="chart-area">
                            <canvas id="chart3" style="display: block; height: 320px;"></canvas>
                        </div>
                    </div>
                    <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解RSI的變化喔～</p>
                </div>

                <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
                    <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
                        <span class="text">回上一頁</span>
                    </a>
                    <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                        <span class="text">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": "chart3",
                "chart_config": None
        },
        {
                "page_index": 8,
                "html_content": """
                <div class="m-4 font-large w-75" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">第五課總結</h2>
                    <ul class="fs-5 mb-4" style="list-style-type:none;">
                        <li>RSI：觀察市場某段時間的漲跌趨勢，用來衡量買賣力道的平衡。</li>
                        <li>學習如何計算 RSI ，若數值在 30～70 之間則屬於<strong>正常波動區。</strong></li>
                    </ul> 
                    <ul class="fs-5 mb-4" style="list-style-type:none;">
                        <li>不只是數字，更要看懂「轉折」<br>➡️ RSI 往上突破 30、往下跌破 70，常常是短線「反轉訊號」的起點。</li>
                    </ul>
                    <ul class="fs-5 mb-4" style="list-style-type:none;">
                        <li>搭配 K 線一起判斷<br>➡️RSI 高檔出現黑K，或 RSI 低檔出現紅K，這些訊號加上價格行為更準確。</li>
                        <li>不要單靠 RSI 做決策！</li>
                    </ul> 

                    <p class="fs-5 mb-4 mt-4 text-center">📌 下一課：布林帶「股價的伸縮彈簧，當價格逼近上下邊界，市場可能準備反彈或回檔！」</p>
                </div>
                <div class="d-flex mb-5 justify-content-center" style="gap: 10%">
                    <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
                        <span class="text">回上一頁</span>
                    </a>
                    <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
                        <span class="text">前往課後練習</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None
        }
]

@course5_api.route('/api/course_content/course5')
def get_course5_content():
    return jsonify({"pages": course5_pages})
