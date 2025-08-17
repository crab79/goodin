from flask import Blueprint, jsonify

course7_api = Blueprint('course7_api', __name__)

# 課程7資料（MACD指標）
course7_pages = [
    {
        "page_index": 0,
        "html_content": """
        <div id="chart-container" class="card shadow mb-4">
          <div class="card-body align-self-center">
            <div class="chart-area"><div class="chartjs-size-monitor"><div class="chartjs-size-monitor-expand"><div class=""></div></div><div class="chartjs-size-monitor-shrink"><div class=""></div></div></div>
                <canvas id="chart1" style="display: block; height: 320px; width: 836px;" width="1003" height="384" class="chartjs-render-monitor"></canvas>
            </div>
          </div>
        </div>
        <div class="m-4 font-large align-self-center">
          <h1 class="fw-bolder mb-4 mt-2">什麼是 MACD？</h1>
          <ul class="fs-5 mb-4">
            <li>平滑異同移動<strong>平均線</strong>（MACD）</li>
            <li>用於判斷股價趨勢的技術指標</li>
            <li>比較短期與長期股價變動速度</li>
          </ul>
        </div>
        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": "chart1",
        "multi_steps": []
    },
    {
        "page_index": 1,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">既然MACD 跟「平均線」有關，那麼平均線有哪些種類呢？</h2>
          <ul class="fs-5 mb-4">
            <li>5MA：過去 5 天股價的平均</li>
            <li>20MA：過去 20 天股價的平均</li>
            <p class="fs-5 mb-4">這些平均值畫出來的線，可以幫助我們看出股價的整體趨勢。</p>
          </ul>
        </div>

        <div id="chart-container" class="card shadow mb-4" style="display:none;">
          <div class="card-body align-self-center">
            <div class="chart-area">
              <canvas id="chart2" style="display: block; height: 320px;"></canvas>
            </div>
          </div>
          <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解平均線的變化喔～</p>
        </div>


        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": "chart2",
        "multi_steps": ["chart-container"]
    },
    {
        "page_index": 2,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">平均會發生什麼事？</h2>
          <p class="fs-5 mb-4">平均有一個「副作用」，就是會把「差異」隱藏掉。</p>
          <p class="fs-5 mb-4">就像你和一位奧運選手一起跑步，平均下來你們的速度看起來都不錯，</p>
          <p class="fs-5 mb-4">但實際上，是他衝得飛快，你在後面喘到不行。</p>
          <p class="fs-5 mb-4">這就是平均造成的假象——表面看起來沒什麼問題，但其實細節差很多。</p>
        </div>

        <div class="d-flex flex-column align-items-center w-75" style="align-self: center;">
          <iframe src="https://giphy.com/embed/2bUpP71bbVnZ3x7lgQ" width="480" height="403" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/reaction-2bUpP71bbVnZ3x7lgQ">via GIPHY</a></p>
        </div>
        
        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": None,
        "multi_steps": []
    },
    {
        "page_index": 3,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">指數移動平均線（EMA）是什麼？</h2>
          <p class="fs-5 mb-4">MACD 使用的不是普通的均線，而是「指數移動平均線（EMA）」。</p>
          <p class="fs-5 mb-4">EMA 的特色是：越接近現在的價格，權重就越高。</p>
          <p class="fs-5 mb-4">就像是你在辦桌吃飯，主桌的來賓會被特別照顧，而遠一點的客人則普通安排。越重要的、越靠近的訊號，權重自然也會提高。</p>
          <p class="fs-5 mb-4">所以，MACD 是一種更「聰明」的均線，能更靈敏地反應股價的變化。</p>
        </div>

        <div class="d-flex flex-column align-items-center w-75" style="align-self: center;">
          <iframe src="https://giphy.com/embed/HdDDyhS3yXs5zio5s0" width="480" height="271" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/MasterChefAU-dessert-masterchef-masterchefau-HdDDyhS3yXs5zio5s0">via GIPHY</a></p>
        </div>
        
        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": None,
        "multi_steps": []
    },
    {
        "page_index": 4,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">MACD 的三個重點：慢線、快線 、OSC 柱狀圖</h2>
          <ul class="fs-5 mb-4">當你在技術分析軟體中打開 MACD 這個指標時，通常會看到：
            <li>兩條線</li>
            <li>一組紅綠相間的柱狀圖</li>
          </ul>
        </div>

        <div id="chart-container" class="card shadow mb-4" style="display:none;">
          <div class="card-body align-self-center">
            <div class="chart-area">
              <canvas id="chart1" style="display: block; height: 320px;"></canvas>
            </div>
          </div>
          <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解MACD的變化喔～</p>
        </div>


        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": "chart1",
        "multi_steps": ["chart-container"]
    },
    {
        "page_index": 5,
        "html_content": """
        <div class="m-4 font-large w-75" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">MACD 的專有名詞其實有差異</h2>
          <p class="fs-5 mb-4">當你使用看盤軟體的時候可以注意一下</p>
          <p class="fs-5 mb-4">國內和國外對於 MACD 的核心計算邏輯是相同的，主要的差異在於名詞的稱呼</p>
          <img src="/static/images/course_macd_1.png" alt="MACD difference table">

        </div>

        
        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": None,
        "multi_steps": []
    },
    {
        "page_index": 6,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">快線(台灣稱DIF、國外稱MACD)</h2>
          <p class="fs-5 mb-4">DIF 是兩條不同期間 EMA 的差值：</p>
          <p class="fs-5 mb-4">DIF = EMA(12) – EMA(26)</p>
          <p class="fs-5 mb-4">簡單說，就是短期平均值和長期平均值的差距。當短期走勢比較強時，DIF 就會往上。</p>
        </div>

        <div id="carousel" class="d-flex flex-column align-items-center w-75 mb-4" style="align-self: center; display: none;"></div>

        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": None,
        "multi_steps": ["carousel"],
        "carousel_items": [
            {
                "src": "/static/images/course_macd_2.png",
                "alt": "TradingView",
                "caption": "以 TradingView 的圖為例，快線是藍線",
                "credit": "圖片來源：<a href=\"https://www.tradingview.com/chart/?symbol=NYSE%3ATSM\" target=\"_blank\">TradingView</a>"
            },
            {
                "src": "/static/images/course_macd_3.png",
                "alt": "玩股網",
                "caption": "以玩股網的圖為例，快線是紅線",
                "credit": "圖片來源：<a href=\"https://www.wantgoo.com/stock/2330/technical-chart\" target=\"_blank\">玩股網</a>"
            }
        ]
    },
    {
        "page_index": 7,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">慢線（國外是Signal、台灣稱MACD ）</h2>
          <p class="fs-5 mb-4">這條線是 DIF 的 9 日 EMA，算是「DIF 的平均線」：</p>
          <p class="fs-5 mb-4">MACD = EMA(DIF, 9)</p>
          <p class="fs-5 mb-4">也有人稱這條為「慢線」，因為它比 DIF 緩慢、平滑</p>
        </div>

        <div id="carousel" class="d-flex flex-column align-items-center w-75 mb-4" style="align-self: center; display: none;"></div>

        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": None,
        "multi_steps": ["carousel"],
        "carousel_items": [
            {
                "src": "/static/images/course_macd_2.png",
                "alt": "TradingView",
                "caption": "以 TradingView 的圖為例，慢線是黃線",
                "credit": "圖片來源：<a href=\"https://www.tradingview.com/chart/?symbol=NYSE%3ATSM\" target=\"_blank\">TradingView</a>"
            },
            {
                "src": "/static/images/course_macd_3.png",
                "alt": "玩股網",
                "caption": "以玩股網的圖為例，慢線是藍線",
                "credit": "圖片來源：<a href=\"https://www.wantgoo.com/stock/2330/technical-chart\" target=\"_blank\">玩股網</a>"
            }
        ]
    },
    {
        "page_index": 8,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">OSC 柱狀圖</h2>
          <p class="fs-5 mb-4">我們看到的紅色、綠色柱子，是用下面這個公式算出來的：</p>
          <p class="fs-5 mb-4">OSC = DIF – MACD</p>
          <p class="fs-5 mb-4">OSC > 0（正值） → 顯示紅色柱子</p>
          <p class="fs-5 mb-4">OSC < 0（負值） → 顯示綠色柱子</p>
          <p class="fs-5 mb-4">這些柱狀圖的長短，能幫助我們觀察趨勢變化的「力度」。</p>
        </div>

        <div id="chart-container" class="card shadow mb-4" style="display:none;">
          <div class="card-body align-self-center w-100">
            <div class="chart-area w-100">
              <canvas id="chart4" style="display: block; height: 320px;"></canvas>
            </div>
          </div>
          <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解柱狀圖的變化喔～</p>
        </div>

        <div id="text-container" class="m-4 font-large flex-column" style="align-self: center;display:none;">
          <h5 class="fs-5 mb-4">OSC 柱狀圖的變化，代表市場動能的強弱：</h5>
          <p class="fs-5 mb-4">柱狀圖變長（無論紅或綠）→ 表示趨勢正在加強，股價容易持續上漲或下跌</p>
          <p class="fs-5 mb-4">柱狀圖縮短 → 表示動能在減弱，股價可能會橫盤整理或轉向</p>
        </div>

        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": "chart4",
        "multi_steps": ["chart-container", "text-container"]
    },
    {
        "page_index": 9,
        "html_content": """
        <div class="m-4 font-large w-75" style="align-self: center;">
          <h2 class="fw-bolder mb-5 mt-2">黃金交叉 vs 死亡交叉</h2>
          <div class="d-flex" style="gap:5%">
              <div class="d-flex flex-column">
                <h5 class="fs-5 mb-4"><strong>黃金交叉</strong></h5>
                <p class="fs-5 mb-4">當 DIF 往上穿越 MACD 線時，形成「黃金交叉」</p>
                <p class="fs-5 mb-4">→ 通常視為股價有轉強、趨勢往上的可能。</p>
              </div>
              <div class="d-flex flex-column">
                <h5 class="fs-5 mb-4"><strong>死亡交叉</strong></h5>
                <p class="fs-5 mb-4">當 DIF 往下跌破 MACD 線時，形成「死亡交叉」</p>
                <p class="fs-5 mb-4">→ 通常視為股價轉弱、可能要下跌了。</p>
              </div>
          </div>
        </div>

        <div id="chart-container" class="card shadow mb-4" style="display:none;">
          <div class="card-body align-self-center w-100">
            <div class="chart-area">
              <canvas id="chart5" style="display: block; height: 320px;"></canvas>
            </div>
          </div>
          <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解兩種交叉的變化喔～</p>
        </div>


        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": "chart5",
        "multi_steps": ["chart-container"]
    },
    {
        "page_index": 10,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">MACD 的限制</h2>
          <p class="fs-5 mb-4">雖然 MACD 是很有參考價值的指標，但它也不是萬能的：</p>
          <ol>
            <li class="fs-5 mb-4">它是「落後指標」</li>
            <p class="fs-5 mb-4">MACD 是根據過去的股價計算出來的，所以反應速度沒那麼快。</p>
            <p class="fs-5 mb-4">很多時候等你看到黃金交叉，股價可能已經漲了一段。</p>
            <li class="fs-5 mb-4">容易誤判橫盤盤整</li>
            <p class="fs-5 mb-4">當股價進入橫盤整理期（不上不下），MACD 的快線和慢線就會頻繁交叉， 這時候你用交叉或柱體長短來判斷趨勢，可能會出現「假訊號」。</p>
          </ol>
        </div>

        <div class="d-flex flex-column align-items-center w-75" style="align-self: center;">
          <iframe src="https://giphy.com/embed/j4ksLmVDR4e6DbSQxU" width="480" height="269" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/PabloTVShow-pablo-pablotvshow-draff-j4ksLmVDR4e6DbSQxU">via GIPHY</a></p>
        </div>
        
        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">繼續</span>
          </a>
        </div>
        """,
        "chart_type": None,
        "multi_steps": []
    },
    {
        "page_index": 11,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
          <h2 class="fw-bolder mb-4 mt-2">總結重點</h2>
          <ul>
            <li class="fs-5 mb-4">黃金交叉 → 趨勢轉強，可能會上漲</li>
            <li class="fs-5 mb-4">死亡交叉 → 趨勢轉弱，可能會下跌</li>
            <li class="fs-5 mb-4">OSC 柱變長 → 動能強，趨勢持續機率高</li>
            <li class="fs-5 mb-4">OSC 柱縮短 → 動能弱，可能進入整理</li>
            <p class="fs-5 mb-4">MACD 是一個幫助我們掌握趨勢方向與強弱的工具，但請記得不要只靠 MACD 做決策，也要搭配其他指標與基本面！</p>
        </div>

        <div class="d-flex flex-column align-items-center w-75" style="align-self: center;">
          <iframe src="https://giphy.com/embed/d3mlE7uhX8KFgEmY" width="480" height="269" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/culture--think-hmm-d3mlE7uhX8KFgEmY">via GIPHY</a></p>
        </div>
        
        <div class="d-flex justify-content-center" style="gap: 10%">
          <a href="#" class="btn btn-dark btn-icon-split w-10 align-self-center" id="prev-btn">
            <span class="text">回上一頁</span>
          </a>
          <a href="#" class="btn btn-info btn-icon-split w-10 align-self-center" id="continue-btn">
            <span class="text">前往課後練習</span>
          </a>
        </div>
        """,
        "chart_type": None,
        "multi_steps": []
    }
]

@course7_api.route('/api/course_content/course7')
def get_course7_content():
    return jsonify({"pages": course7_pages})
