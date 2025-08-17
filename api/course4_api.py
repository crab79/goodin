from flask import Blueprint, jsonify

course4_api = Blueprint('course4_api', __name__)

# 課程4資料（可直接編輯，日後可改為資料庫讀取）
course4_pages = [
        {
                "page_index": 0,
                "html_content": """
                <div class="m-4 font-large align-self-center">
                    <h1 class="fw-bolder mb-4 mt-2 pl-3" style="">簡單移動平均線（SMA, Simple Moving Average）</h1>
                    <ul class="fs-5 mb-4">
                        <li>一種常用的技術指標</li>
                        <li>計算「過去一段期間內」的收盤價平均值</li>
                        <li>過濾掉短期價格波動的「雜訊」</li>
                        <li>平滑價格數據，更清楚的顯示出股票價格的整體走勢</li>
                    </ul>
                </div>
                <div id="chart-container" class="card shadow mb-4" style="display:flex;">
                    <div class="card-body align-self-center">
                        <div class="chart-area">
                            <canvas id="chart1" style="display: block; height: 320px;"></canvas>
                        </div>
                    </div>
                    <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解SMA的變化喔～</p>
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
                    <h1 class="fw-bolder mb-4 mt-2 pl-5">為何要使用SMA？</h1>
                    <ul class="fs-5 mb-4" style="list-style-type: none;">
                        <li class="fs-5 mb-4">濾除雜訊
                            <ul style="">
                                <li>股價無時無刻都在波動，SMA 能幫助我們過濾掉短期波動，讓趨勢更清晰。</li>
                            </ul>
                        </li>
                        <li class="fs-5 mb-4">協助判斷買進賣出的時機
                            <ul style="">
                                <li>當股價突破 SMA，可能代表趨勢轉強，是可以買進的訊號。</li>
                                <li>當股價跌破 SMA，可能是警訊，要開始觀察是否反轉。</li>
                            </ul>
                        </li>
                        <li class="fs-5 mb-4">視覺化分析
                            <ul style="">
                                <li>用線條呈現過去平均價格，搭配 K 線圖觀察，會比單純看股價數字容易理解。</li>
                                <li>多條 SMA（如 5 日與 20 日交叉）還可以進一步做策略分析。</li>
                            </ul>
                        </li>
                    </ul>
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
                "page_index": 2,
                "html_content": """
                <div class="m-4 font-large align-self-center">
                    <h1 class="fw-bolder mb-4 mt-2 pl-5">簡單移動平均線的概念</h1>
                    <ul class="fs-5 mb-4" style="list-style-type: none;">
                        <li>🧠 用日常生活來理解：
                        <ul>
                            <li>想像你每天記錄自己走路的步數</li>
                            <li>然後計算「最近 5 天的平均步數」</li>
                            <li>就可以看出自己最近是越走越多，還是越來越懶。</li>
                        </ul>
                        </li>
                    </ul>
                    <p class="fs-5 mb-4"> 👉 SMA 就像是這樣的「平均步數」，幫助你平滑掉每天的波動，找出結論。</p>
                </div>
                <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
                    <iframe src="https://giphy.com/embed/73bnJru6zWBuBmfE3P" width="480" height="269" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/adultswim-cowboy-bebop-toonami-lazarus-73bnJru6zWBuBmfE3P">via GIPHY</a></p>    
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
                <div class="m-4 font-large" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">計算公式與應用</h2>
                    <p class="fs-5">移動平均線的計算公式(以日K線介紹) : </p>
                    <p class="fs-5"><strong>N日移動平均線 = N日收盤價的總和 ÷ N日</strong></p>
                    <ul class="fs-5 mb-4 p-0" style="list-style-type:none;">例如：
                        <li>5日均線就是把過去5天的收盤價加總再除以5。</li>
                        <li>20日均線就是把過去20天的收盤價加總再除以20。</li>
                        <li>計算的時候會包含當天（第n日）的收盤價喔～</li>
                    </ul>    
                </div>

                <div id="chart-container" class="card shadow p-4 mb-4 align-content-center" style="display:none;">
                    <div class="card-body align-self-center">
                        <div class="chart-area">
                            <canvas id="chart2" style="display: block; height: 320px;"></canvas>
                        </div>
                    </div>
                    <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解SMA的變化喔～</p>
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
                "chart_type": "chart2",
                "chart_config": None,
                "multi_steps": ["chart-container"]
        },
        {
                "page_index": 4,
                "html_content": """
                <div class="m-4 font-large pl-5" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">在實務中的應用小技巧</h2>
                    <p class="fs-5 mb-4">📈 黃金交叉（Golden Cross）</p>
                    <ul class="fs-5 mb-4">
                        <li>當短期均線（ 5 日）向上穿越長期均線（ 20 日）→ <strong>可能是股價上漲的開始</strong></li>
                    </ul>
                    <p class="fs-5 mb-4">📉 死亡交叉（Death Cross）</p>
                    <ul class="fs-5 mb-4">
                        <li>當短期均線（ 5 日）向下跌破長期均線 （ 20 日）→ <strong>常被視為空頭訊號，投資人大多會轉為保守或賣出</strong></li>
                    </ul>   
                    <img  src="https://static.wealth.com.tw/746c361b7836a2b3ae6eaaf985fb80fde42508d3.png" alt="cross types" style="max-width:80vw;">  
                    <p class="mt-4 w-75 text-muted medium" style="text-align:right;">
                        圖片來源：<a href="https://www.wealth.com.tw/articles/15331489-0c3b-4ef6-a197-0c5262784872" target="_blank">
                                黃金交叉、死亡交叉是什麼？2張圖看懂買進賣出訊號！
                        </a>
                    </p>  
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
                "page_index": 5,
                "html_content": """
                <div class="m-4 font-large" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">圖表示範</h2>
                </div>

                <div id="chart-container" class="card shadow mb-4" style="display:flex;">
                    <div class="card-body align-self-center">
                        <div class="chart-area">
                            <canvas id="chart3" style="display: block; height: 320px;"></canvas>
                        </div>
                    </div>
                </div>
                <p class="fs-5 mb-4 align-self-center">黃金交叉發生在短期均線（藍色線）<strong>從下往上</strong>穿越長期均線（橘色線）的那一條K線。</p>
                <p class="fs-5 mb-4 align-self-center">死亡交叉發生在短期均線（藍色線）<strong>從上往下</strong>穿越長期均線（橘色線）的那一條K線。</p>
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
                "page_index": 6,
                "html_content": """
                <div class="m-4 font-large w-75" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">SMA的常見問題</h2>
                    <p class="fs-5 mb-4">📌 常見問題</p>
                    <ul class="fs-5 mb-4" style="list-style-type:none;">
                        <li>Q：SMA 有用嗎？會不會太慢？</li>
                        <li>A：SMA 是用來觀察整體趨勢的工具，比較不適合做超短線操作。
                        建議搭配其他指標（如 RSI、MACD），會更有效。</li>
                    </ul> 
                    <div id="text1" style="display:none;">
                    <ul class="fs-5 mb-4" style="list-style-type:none;">
                        <li>Q：該選用幾日的 SMA？</li>
                        <li> A：可依照你的操作習慣調整：
                            <ul>
                                <li>短線交易者：5 日、10 日</li>
                                <li>波段交易者：20 日、60 日</li>
                                <li>長期投資者：120 日、240 日</li>
                            </ul>
                        </li>
                    </ul> 
                </div>
                </div>

                <div class="flex-column align-items-center w-75  pl-5" style="align-self: center; display:none;" id="text2">
                    <iframe src="https://giphy.com/embed/rHRe82VaiiaMMPzTrc" width="480" height="300" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/SappySeals-rHRe82VaiiaMMPzTrc">via GIPHY</a></p>
                </div>

                <div id="text3" class="w-75 m-4 font-large" style="align-self: center;display:none;">
                    <ul class="fs-5 mb-4" style="list-style-type:none;">
                        <li>📌 小提醒</li>
                        <li> SMA 是落後指標，它反應的是「過去」的價格。</li>
                        <li>數字越大的 SMA 趨勢越穩定，<strong>反應越慢</strong></li>
                        <li>數字越小則越靈敏，<strong>容易受干擾</strong></li>
                    </ul>
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
                "multi_steps": ["text1", "text2", "text3"]
        },
        {
                "page_index": 7,
                "html_content": """
                <div class="m-4 font-large pl-5" style="align-self: center;">
                    <h2 class="fw-bolder mb-4 mt-2">第四課總結</h2>
                    <p class="fs-5 mb-4">K線是什麼？</p>
                    <ul class="fs-5 mb-4">
                        <li>SMA 將過去 N 天的股價平均，幫助我們「看見趨勢」，濾除雜訊。</li>
                        <li>學習如何計算 SMA（例如 5 日、20 日）</li>
                        <li>看懂「黃金交叉」、「死亡交叉」代表的意思與警訊</li>
                        <li>學會從線的方向，判斷市場氣氛（上升/下降）</li>
                    </ul>   
                    <p class="fs-5 mb-4 mt-4">SMA 就像投資地圖的導航線，雖然不告訴你終點在哪，但能幫你避開顛簸的路。</p>
                </div>
                <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
                    <iframe src="https://giphy.com/embed/iwRTtutqiv9UdWHgxi" width="414" height="480" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/iqoption-cute-cartoon-loop-iwRTtutqiv9UdWHgxi">via GIPHY</a></p>
                </div>
                <p class="fs-5 mb-4" style="text-align:center">📌 下一課：RSI 相對強弱指標「高檔賣壓？低檔超跌？RSI 一眼看出關鍵反轉點！」💪📈</p>


                <div class="d-flex justify-content-center mb-5" style="gap: 10%">
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

@course4_api.route('/api/course_content/course4')
def get_course4_content():
    return jsonify({"pages": course4_pages})
