from flask import Blueprint, jsonify

course9_api = Blueprint('course9_api', __name__)

# 課程9資料（乖離率 BIAS）
course9_pages = [
    {
        "page_index": 0,
        "html_content": """
        <div class="m-4 font-large align-self-center">
            <h1 class="fw-bolder mb-4 mt-2" style="">什麼是乖離率？</h1>
            <p class="fs-5 mb-2">想像你在跑馬拉松，通常你會按照自己習慣的步調前進。<br>乖離率能幫助你判斷現在是「過快可能會累倒」，還是「過慢可能要加速」，讓你維持穩定的節奏。</p>
        </div>
        <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
            <iframe src="https://giphy.com/embed/H7wDWXvJhjtkn6QURb" width="480" height="480" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/TeamUSA-usa-olympic-team-olympics-H7wDWXvJhjtkn6QURb">via GIPHY</a></p>
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
        "page_index": 1,
        "html_content": """
        <div class="m-4 font-large align-self-center">
            <h1 class="fw-bolder mb-4 mt-2">什麼是乖離率？</h1>
            <p class="fs-5 mb-2">在股市中，乖離率用來衡量價格與移動平均線的偏離程度，告訴我們價格是否過高（超買）或過低（超賣）。</p>
            <img  src="https://storage.googleapis.com/oanda-prod-asne1-oj-tw-wordpress/2022/01/0127001.png" alt="cross types" style="max-width:80vw;">  
            <p class="mt-4 w-75 text-muted medium">
                圖片來源：<a href="https://www.oanda.com/bvi-ft/lab-education/technical_analysis/bias/" target="_blank">
                    乖離率(BIAS)的交易策略解析 
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
        "page_index": 2,
        "html_content": """
        <div class="m-4 font-large align-self-center">
            <h1 class="fw-bolder mb-4 mt-2"> 熊市與牛市的概念</h1>
            <p class="fs-5 mb-2">在學習乖離率之前，我們需要先了解「熊市」和「牛市」這兩個基本概念</p>
        </div>
        <div id="carousel" class="d-flex flex-column align-items-center w-75 mb-4" style="align-self: center; display: none;"></div>
        <p class="fs-5 mb-4 text-center" style="display:none;" id="text1"> 🐂 牛市（Bull Market）：市場處於上升趨勢，投資者樂觀，股價普遍呈現長期上漲的趨勢。就像一隻牛向前衝，推動市場不斷上升。</p>
        <p class="fs-5 mb-4 text-center" style="display:none;" id="text2"> 🐻 熊市（Bear Market）：市場處於下降趨勢，投資者悲觀，股價持續下跌。這就像熊站起來然後向下揮動爪子，象徵市場走低。</p>
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
        "multi_steps": ["carousel", "text1", "text2"],
        "carousel_items": [
            {
                "src": "https://assets.cmcmarkets.com/images/Bull-market_extra.webp",
                "alt": "Bull Market",
                "caption": "牛市（Bull Market）",
                "credit": "圖片來源：<a href=\"https://www.cmcmarkets.com/en-gb/trading-guides/bull-markets\" target=\"_blank\">What is a bull market and what have been the biggest in history?</a>"
            },
            {
                "src": "https://wallstreettreasures.com/cdn/shop/products/532012_720x.jpg?v=1613055710",
                "alt": "Bear Market",
                "caption": "熊市（Bear Market）",
                "credit": "圖片來源：<a href=\"https://wallstreettreasures.com/products/6-inch-wall-street-bear-statue?srsltid=AfmBOoqgxYuNZEOCrTC_A81TZ8M8nTma4JI1d60OqA_yyVQ-7pDvAQov\" target=\"_blank\">Wall Street Treasures</a>"
            }
        ]
    },
    {
        "page_index": 3,
        "html_content": """
        <div class="m-4 font-large align-self-center w-100">
            <h1 class="fw-bolder mb-4 mt-2"> 熊市與牛市的概念</h1>
            <ul class="fs-5 mb-4">
                <li>在牛市中，乖離率可能會長期維持高檔<br>而在熊市中，乖離率可能會持續維持低位，因此判斷趨勢方向很重要，避免錯誤解讀買賣訊號。</li>
                <li>道瓊工業指數歷史走勢，除了2008年金融海嘯、2020年新冠疫情外，幾乎以牛市為主。</li>
            </ul>
            <img  src="https://s.yimg.com/ny/api/res/1.2/WouIv9_DSTp4H_EgCLZU2w--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTU0MA--/https://s.yimg.com/os/creatr-uploaded-images/2022-05/1dd664d0-da63-11ec-bf77-87a065a04b89" alt="cross types" style="max-height:50vh;max-width:80vw;">  
            <p class="mt-4 text-muted medium" style="text-align:center;">
                圖片來源：<a href="https://tw.stock.yahoo.com/news/%E7%86%8A%E5%B8%82-%E7%89%9B%E5%B8%82-%E4%BD%8E%E9%BB%9E%E4%BD%88%E5%B1%80-%E8%82%A1%E5%B8%82%E5%8F%8D%E5%BD%88-065659324.html" target="_blank">
                    全球股市邁入熊市！牛市、熊市如何定義？熊市如何佈局？維持多久？熊市何時反彈？
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
        "page_index": 4,
        "html_content": """
        <div class="m-4 font-large align-self-center w-100">
            <h1 class="fw-bolder mb-4 mt-2"> 為什麼要學乖離率？</h1>
            <p class="fs-5 mb-2" id="text1">預測市場過熱或超跌： 就像天氣預報，乖離率能幫助投資者避開過熱或過度恐慌的市場。</p>
            <p class="fs-5 mb-2" id="text2" style="display:none;">幫助決定進出場時機： 當乖離率過高時，可能意味著價格「跑太快」，需要喘口氣；當乖離率過低時，則可能代表價格「太疲軟」，準備反彈。</p>
            <p class="fs-5 mb-2" id="text3" style="display:none;">簡單直觀，適合新手： 乖離率的計算方式簡單，新手也能輕鬆理解並運用。</p>
            <div class="flex-column align-items-center pl-5" style="align-self;display:flex;" id="gif1">
                <iframe src="https://giphy.com/embed/JP19C9y60fotQgOdkn" width="480rem" height="480rem" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/weatherchannel-twc-the-weather-channel-JP19C9y60fotQgOdkn">via GIPHY</a></p>
            </div>
            <div class="flex-column align-items-center pl-5" style="align-self: center;display:none;" id="gif2">
                <iframe src="https://giphy.com/embed/WqmYGa2LjQlTG" width="480rem" height="329rem" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/cat-funny-WqmYGa2LjQlTG">via GIPHY</a></p>
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
        "multi_steps": ["text2_text3_gif2"]
    },
    {
        "page_index": 5,
        "html_content": """
        <div class="m-4 font-large w-100" style="align-self: center;">
            <h2 class="fw-bolder mb-4 mt-2">乖離率怎麼算？</h2>
            <p class="fs-5 mb-2">乖離率（Bias Ratio）計算公式：</p>
            <div class="fs-5 mb-2 w-100" style="text-align: center;"> 
                $$ \\text{乖離率}(\\%) = \\left[ \\frac{\\text{當前價格} - \\text{平均價格}}{\\text{平均價格}} \\right] \\times 100\\% $$
            </div>
            <p class="fs-5 mb-2">舉例來說，如果今天股價是 50 元，而 10 天平均股價是 45 元：</p>
            <div class="fs-5 mb-2 w-10" style="text-align: center;">
                $$ \\text{乖離率}(10\\text{天}) = \\left[ \\frac{50 - 45}{45} \\right] \\times 100\\% = 11.11\\% $$
            </div>
            <img  src="https://img.rich01.com/wp-content/uploads/2024/08/20240807102253_0_c06fd3.jpg" alt="cross types" style="max-width:50vw;">  
            <p class="mt-4 text-muted medium" style="text-align:center;">
                圖片來源：<a href="https://rich01.com/what-is-bias-ratio/" target="_blank">
                    乖離率是什麼？代表意義/計算與查詢方式/運用注意事項介紹
                </a>
            </p> 
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
        "chart_config": None
    },
    {
        "page_index": 6,
        "html_content": """
        <div class="m-4 font-large w-100" style="align-self: center;">
            <h2 class="fw-bolder mb-4 mt-2">怎麼判斷買賣時機</h2>
            <ul class="fs-5 mb-4">
                <li>乖離率過高（+10% 或以上） → 市場可能「跑過頭」，有回調風險，可能需要放慢步伐。</li>
                <li>乖離率過低（-10% 或以下） → 市場可能「跌過頭」，有機會反彈，就像你體力恢復後準備加速。</li>
                <li>乖離率回歸均線 → 價格趨於穩定，適合觀察市場是否進入新的趨勢。</li>
            </ul>
            <img  src="https://storage.googleapis.com/oanda-prod-asne1-oj-tw-wordpress/2022/01/0127002.png" alt="cross types" style="max-height:50vh;max-width:100%">  
            <p class="mt-4 text-muted medium" style="text-align:center;">
                圖片來源：<a href="https://www.oanda.com/bvi-ft/lab-education/technical_analysis/bias/" target="_blank">
                    乖離率(BIAS)的交易策略解析 
                </a>
            </p> 
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
        "chart_config": None
    },
    {
        "page_index": 7,
        "html_content": """
        <div class="m-4 font-large" style="align-self: center;">
            <h2 class="fw-bolder mb-4 mt-2">乖離率的優點</h2>
            <ul class="fs-5 mb-4">
                <li>直觀易懂，可快速判斷市場過熱或超跌。</li>
                <li>在震盪行情中，常能提供短線交易機會。</li>
                <li>能與其他技術指標（如 MACD、KD 指標）搭配，提高分析準確性。</li>
            </ul>
        </div>
        <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
            <iframe src="https://giphy.com/embed/tRq6FAwaKDQIzWwMWr" width="480" height="269" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/chikawa-kurimanju-tRq6FAwaKDQIzWwMWr">via GIPHY</a></p>
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
        "chart_config": None
    },
    {
        "page_index": 8,
        "html_content": """
        <div class="m-4 font-large align-self-center">
            <h1 class="fw-bolder mb-4 mt-2 pl-3" style="">乖離率的缺點</h1>
            <p class="fs-5 mb-2">在長期單邊行情中，乖離率可能長期維持高位或低位，出現「鈍化」現象。</p>
            <p class="fs-5 mb-2">若市場極端強勢或弱勢，價格可能持續偏離均線，使乖離率的參考價值下降。</p>
        </div>
        <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
            <iframe src="https://giphy.com/embed/nR4L10XlJcSeQ" width="480" height="413" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/no-cat-nR4L10XlJcSeQ">via GIPHY</a></p>
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
        "chart_config": None
    },
    {
        "page_index": 9,
        "html_content": """
        <div class="m-4 font-large align-self-center">
            <h1 class="fw-bolder mb-4 mt-2" style="">進階應用</h1>
        </div>

        <div id="chart-container" class="card shadow mb-4" style="display:flex;">
            <div class="card-body align-self-center">
                <div class="chart-area">
                    <canvas id="chart1" style="display: block; height: 320px;"></canvas>
                </div>
            </div>
            <p class="fs-5 mb-4 align-self-center">你可以操作圖表來更了解kd的變化喔～</p>
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
        "chart_type": "chart1",
        "chart_config": None
    },
    {
        "page_index": 10,
        "html_content": """
        <div class="m-4 font-large align-self-center">
            <h1 class="fw-bolder mb-4 mt-2" style="">進階應用</h1>
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
        "page_index": 11,
        "html_content": """
        <div class="m-4 font-large align-self-center">
            <h1 class="fw-bolder mb-4 mt-2" style="">進階應用</h1>
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
        "page_index": 12,
        "html_content": """
        <div class="m-4 font-large align-self-center">
            <h1 class="fw-bolder mb-4 mt-2" style="">課程總結</h1>
            <p class="fs-5 mb-2">乖離率是一個有用的技術分析工具，就像跑步時看心率一樣，能幫助你判斷當前的市場節奏。<br>但需搭配其他技術指標，如 MACD、RSI 或均線趨勢(其他單元)，才能做出更精準的投資決策。</p>
            <p class="fs-5 mb-2">多做練習，掌握市場節奏，你就能更準確地預測市場變化！📈</p>
        </div>
        <div class="d-flex flex-column align-items-center w-75  pl-5" style="align-self: center;">
            <iframe src="https://giphy.com/embed/wFnsqjQ5y2OkhCfVvc" width="480" height="269" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/chiikawa-wFnsqjQ5y2OkhCfVvc">via GIPHY</a></p>
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

@course9_api.route('/api/course_content/course9')
def get_course9_content():
    return jsonify({"pages": course9_pages})
