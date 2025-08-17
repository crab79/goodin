from flask import Blueprint, jsonify

course3_api = Blueprint('course3_api', __name__)

# 課程3資料（可直接編輯，日後可改為資料庫讀取）
course3_pages = [
        {
                "page_index": 0,
                "html_content": """
                <div class=\"m-4 font-large align-self-center\">
                    <h1 class=\"fw-bolder mb-4 mt-2 pl-3\">K 線圖是什麼？</h1>
                    <ul class=\"fs-5 mb-4\">
                        <li>股市中常見的圖表，幫助我們觀察股價的變化與市場情緒。</li>
                        <li>就像海上的浪潮，不能預測未來，但能反映當下的市場風向。</li>
                        <li>💡 小提醒：K 線圖不是「預測神器」，而是「觀察工具」。</li>
                        <img src=\"https://fsv.cmoney.tw/cmstatic/learn/content/44/20141203120757829_XL.jpg\" alt=\"candlestick chart\" class=\"w-75 mt-3\">
                        <p class=\"mt-4 w-75 text-muted medium\">
                        圖片來源：<a href=\"https://www.cmoney.tw/learn/course/technicals/topic/489\" target=_blank>
                                K線是什麼意思？上下影線怎麼看？5張紅黑K棒型態K線圖帶你破解！
                        </a>
                        </p> 
                    </ul>
                </div>
                <div class=\"d-flex justify-content-center mb-5 pr-5\">
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None
        },
        {
                "page_index": 1,
                "html_content": """
                <div class=\"m-4 font-large align-self-center\">
                    <h1 class=\"fw-bolder mb-4 mt-2 pl-5\">K 線怎麼看？</h1>
                    <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">
                        <li>實體（Body）：收盤價與開盤價的區間。
                            <ul>
                                <li>🔴紅 K：收盤價 &gt; 開盤價（上漲）</li>
                                <li>⚫️黑 K：收盤價 &lt; 開盤價（下跌）</li>
                            </ul>
                        </li>
                        <li>影線（Wick）：當日股價的波動範圍（最高價與最低價）</li>
                    </ul>
                </div>
                <div class=\"d-flex flex-column font-large align-items-center\">
                        <img src=\"https://img.rich01.com/wp-content/uploads/20230217084025_89.jpg\" alt=\"candlestick chart\" class=\"w-75 mt-3\">
                        <p class=\"mt-4 w-75 text-muted medium text-center\">
                        圖片來源：<a href=\"https://rich01.com/what-is-k-bar-charts/\" target=_blank>
                                K線是什麼？K線圖怎麼看？K線的16種型態介紹
                        </a>
                        </p>
                </div>
                <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None
        },
        {
                "page_index": 2,
                "html_content": """
                <div class=\"m-4 font-large align-self-center\">
                    <h1 class=\"fw-bolder mb-4 mt-2 pl-5\">K 線怎麼看？</h1>
                    <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">
                        <li>📊 K 線 = 開盤價、收盤價、最高價、最低價組成的四個價格。</li>
                        <li>🌀 股價就像潮水起伏，K 線像是海水的水位變化，讓你看出漲退的趨勢。</li>
                    </ul>
                </div>
                <div class=\"d-flex flex-column font-large align-items-center\">
                        <img src=\"https://img.rich01.com/wp-content/uploads/20230217084025_89.jpg\" alt=\"candlestick chart\" class=\"w-75 mt-3\">
                        <p class=\"mt-4 w-75 text-muted medium text-center\">
                        圖片來源：<a href=\"https://rich01.com/what-is-k-bar-charts/\" target=_blank>
                                K線是什麼？K線圖怎麼看？K線的16種型態介紹
                        </a>
                        </p>
                </div>
                <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None
        },
        {
                "page_index": 3,
                "html_content": """
                <div class=\"m-4 font-large\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">多空力量與K線解讀</h2>
                    <p class=\"fs-5 mb-4\">K線不只是圖形，它背後隱含了市場參與者的心理與力量：</p>
                    <ul class=\"fs-5 mb-4\">
                        <li>多方（買方）：預期上漲，積極買進。</li>
                        <li>空方（賣方）：預期下跌，選擇賣出。</li>
                    </ul>      
                </div>
                <div id=\"chart-container\" class=\"card shadow mb-4\" style=\"display:none;\">
                    <div class=\"card-body align-self-center\">
                        <div class=\"chart-area\">
                            <canvas id=\"chart1\" style=\"display: block; height: 320px;\"></canvas>
                        </div>
                    </div>
                    <p class=\"fs-5 mb-4 align-self-center\">你可以操作圖表來更了解K線圖的變化喔～</p>
                </div>

                <div id=\"text\" class=\"m-4 font-large flex-column\" style=\"align-self: center;display:none;\">
                    <ul class=\"fs-5 mb-4\">
                        <li>長紅 K 線：多方強勢，股價一路上揚。</li>
                        <li>長黑 K 線：空方主導，股價下挫。</li>
                        <li>上影線長：價格上攻受壓，賣壓大。</li>
                        <li>下影線長：價格下探反彈，買盤強。</li>
                    </ul> 
                    <p class=\"fs-5 mb-4\" style=\"align-self: center;\">👊 就像是一場拔河，誰的力量強，股價就往哪裡走。</p>     
                </div>

                <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": "chart1",
                "chart_config": None,
                "multi_steps": ["chart-container", "text"]
        },
        {
                "page_index": 4,
                "html_content": """
                <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">K線的優點和限制</h2>
                    <p class=\"fs-5 mb-4\">🌟 優點：</p>
                    <ul class=\"fs-5 mb-4\">
                        <li>能清楚反映市場情緒和價格波動</li>
                        <li>適用於短中長期趨勢分析</li>
                    </ul>      
                    <div class=\"d-flex flex-column align-items-center w-75  pl-5\" style=\"align-self: center;\">
                        <iframe src=\"https://giphy.com/embed/11ISwbgCxEzMyY\" width=\"480rem\" height=\"360rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/reaction-mrw-11ISwbgCxEzMyY\">via GIPHY</a></p>
                    </div>
                    <div id=\"text\" class=\"flex-column\" style=\"display:none;\">
                        <hr style=\"width:100%;\"></hr>
                        <p class=\"fs-5 mb-4\">⚠️ 限制：</p>
                        <ul class=\"fs-5 mb-4\">
                            <li> 容易受市場雜訊干擾</li>
                            <li>長黑 K 線：空方主導，股價下挫。</li>
                            <li>K 線形態非絕對，需搭配其他指標</li>
                        </ul>  
                        <div class=\"d-flex flex-column align-items-center w-75\" style=\"align-self: center;\">
                            <iframe src=\"https://giphy.com/embed/2H67VmB5UEBmU\" width=\"480rem\" height=\"269rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/movie-mrw-see-2H67VmB5UEBmU\">via GIPHY</a></p>
                        </div>
                        <p class=\"fs-5 mb-4\">🌀K線就像天氣預報，雖然不能保證準確，但能提供參考方向！</p>    
                 </div>
                </div>

                <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["text"]
            },
            {
                "page_index": 5,
                "html_content": """
                <div class=\"m-4 font-large\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">常見價格型態圖解與說明</h2>
                    <ul class=\"fs-5 mb-4\">
                        <li>頭肩頂：『左肩-頭-右肩』型態，可能反轉下跌。</li>
                        <li>雙重頂（M 頭）：出現在上升趨勢尾端，顯示漲勢力道不足。</li>
                    </ul> 
                </div>
                <div id=\"carousel\" class=\"d-flex flex-column align-items-center w-75 mb-4 p-3\" style=\"align-self: center; display: none;\"></div>

                <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["carousel"],
                "carousel_items": [
                    {
                        "src": "https://quantpass.org/wp-content/uploads/2024/03/012_vivipic.webp",
                        "alt": "頭肩頂",
                        "caption": "頭肩頂：『左肩-頭-右肩』型態，可能反轉下跌。",
                        "credit": "圖片來源：<a href=\"https://quantpass.org/kbar-pattern-3/#DoubleTop\" target=\"_blank\">一招找出頭肩底與三角收斂，11種常見的組合K線型態｜頭肩頂、W底、M頭、楔形｜K棒型態學（三）</a>"
                    },
                    {
                        "src": "https://quantpass.org/wp-content/uploads/2024/03/014_vivipic.webp",
                        "alt": "雙重頂（M 頭）",
                        "caption": "雙重頂（M 頭）：出現在上升趨勢尾端，顯示漲勢力道不足。",
                        "credit": "圖片來源：<a href=\"https://quantpass.org/kbar-pattern-3/#DoubleTop\" target=\"_blank\">一招找出頭肩底與三角收斂，11種常見的組合K線型態｜頭肩頂、W底、M頭、楔形｜K棒型態學（三）</a>"
                    }
                ]
            },
            {
                "page_index": 6,
                "html_content": """
                <div class=\"m-4 font-large\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">常見價格型態圖解與說明</h2>
                    <ul class=\"fs-5 mb-4\">
                        <li>雙底（W 型）：下跌後反彈，可能是反轉訊號。</li>
                        <li>圓底：價格緩跌後緩升，屬於溫和築底。</li>
                    </ul> 
                </div>
                <div id=\"carousel\" class=\"d-flex flex-column align-items-center w-75 mb-4 p-3\" style=\"align-self: center; display: none;\"></div>

                <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["carousel"],
                "carousel_items": [
                    {
                        "src": "https://quantpass.org/wp-content/uploads/2024/03/015_vivipic.webp",
                        "alt": "雙底（W 型）",
                        "caption": "雙底（W 型）：下跌後反彈，可能是反轉訊號。",
                        "credit": "圖片來源：<a href=\"https://quantpass.org/kbar-pattern-3/#DoubleTop\" target=\"_blank\">一招找出頭肩底與三角收斂，11種常見的組合K線型態｜頭肩頂、W底、M頭、楔形｜K棒型態學（三）</a>"
                    },
                    {
                        "src": "https://quantpass.org/wp-content/uploads/2024/03/017_vivipic.webp",
                        "alt": "圓底",
                        "caption": "圓底：價格緩跌後緩升，屬於溫和築底。",
                        "credit": "圖片來源：<a href=\"https://quantpass.org/kbar-pattern-3/#DoubleTop\" target=\"_blank\">一招找出頭肩底與三角收斂，11種常見的組合K線型態｜頭肩頂、W底、M頭、楔形｜K棒型態學（三）</a>"
                    }
                ]
            },
            {
                "page_index": 7,
                "html_content": """
                <div class=\"m-4 font-large\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">常見價格型態圖解與說明</h2>
                    <ul class=\"fs-5 mb-4\">
                        <li>杯柄：像茶杯型態，通常在上漲趨勢中出現。</li>
                        <li>V 型反轉：價格急跌後迅速反彈，雖上漲速度快但反轉風險較高。</li>
                    </ul> 
                </div>
                <div id=\"carousel\" class=\"d-flex flex-column align-items-center w-75 mb-4 p-3\" style=\"align-self: center; display: none;\"></div>

                <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["carousel"],
                "carousel_items": [
                    {
                        "src": "https://scanz.com/wp-content/uploads/2019/01/cupandhandlepatternrecognition.jpg",
                        "alt": "杯柄",
                        "caption": "杯柄：像茶杯型態，通常在上漲趨勢中出現。",
                        "credit": "圖片來源：<a href=\"https://scanz.com/cup-and-handle-patterns/\" target=\"_blank\">A Comprehensive Guide to Cup and Handle Patterns</a>"
                    },
                    {
                        "src": "https://quantpass.org/wp-content/uploads/2024/03/022_vivipic.webp",
                        "alt": "V 型反轉",
                        "caption": "V 型反轉：價格急跌後迅速反彈，雖上漲速度快但反轉風險較高。",
                        "credit": "圖片來源：<a href=\"https://quantpass.org/kbar-pattern-3/#DoubleTop\" target=\"_blank\">一招找出頭肩底與三角收斂，11種常見的組合K線型態｜頭肩頂、W底、M頭、楔形｜K棒型態學（三）</a>"
                    }
                ]
            },
            {
                "page_index": 8,
                "html_content": """
                <div class=\"m-4 font-large\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">常見價格型態圖解與說明</h2>
                    <ul class=\"fs-5 mb-4\">
                        <li>旗形：上漲或下跌後的盤整期。</li>
                        <li>楔形：價格收斂型態，觀察突破方向。</li>
                    </ul> 
                </div>
                <div id=\"carousel\" class=\"d-flex flex-column align-items-center w-75 mb-4 p-3\" style=\"align-self: center; display: none;\"></div>

                <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": None,
                "chart_config": None,
                "multi_steps": ["carousel"],
                "carousel_items": [
                    {
                        "src": "https://quantpass.org/wp-content/uploads/2024/03/020_vivipic.webp",
                        "alt": "旗形",
                        "caption": "旗形：上漲或下跌後的盤整期。",
                        "credit": "圖片來源：<a href=\"https://quantpass.org/kbar-pattern-3/#DoubleTop\" target=\"_blank\">一招找出頭肩底與三角收斂，11種常見的組合K線型態｜頭肩頂、W底、M頭、楔形｜K棒型態學（三）</a>"
                    },
                    {
                        "src": "https://quantpass.org/wp-content/uploads/2024/03/019_vivipic.webp",
                        "alt": "楔形",
                        "caption": "楔形：價格收斂型態，觀察突破方向。",
                        "credit": "圖片來源：<a href=\"https://quantpass.org/kbar-pattern-3/#DoubleTop\" target=\"_blank\">一招找出頭肩底與三角收斂，11種常見的組合K線型態｜頭肩頂、W底、M頭、楔形｜K棒型態學（三）</a>"
                    }
                ]
            },
            {
                    "page_index": 9,
                    "html_content": """
                    <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
                        <h2 class=\"fw-bolder mb-4 mt-2\">重點回顧</h2>
                        <p class=\"fs-5 mb-4\">K線是什麼？</p>
                        <ul class=\"fs-5 mb-4\">
                            <li>是一種顯示股價波動的圖表，幫助投資人看懂市場情緒與趨勢。</li>
                        </ul>   
                        <p class=\"fs-5 mb-4\">有什麼用途？</p>
                        <ul class=\"fs-5 mb-4\">
                            <li>用來觀察多空力量、判斷趨勢方向、找出可能的買賣時機。</li>
                        </ul>    
                        <div class=\"d-flex flex-column align-items-center w-75  pl-5\" style=\"align-self: center;\">
                            <iframe src=\"https://giphy.com/embed/e06Wc1bfzPQXnXyhLW\" width=\"480\" height=\"480\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/SVT-david-sundin-bst-i-test-e06Wc1bfzPQXnXyhLW\">via GIPHY</a></p>
                        </div>
                        <div id=\"text\" class=\"flex-column\" style=\"display:none;\">
                            <hr style=\"width:100%;\"></hr>
                            <p class=\"fs-5 mb-4\">要注意什麼？</p>
                            <ul class=\"fs-5 mb-4\">
                                <li>K 線只是工具，不保證預測準確。</li>
                                <li>單一 K 線參考價值有限，要搭配整體趨勢與其他指標使用。</li>
                                <li>解讀重點在於了解市場情緒，而非死記圖形！</li>
                            </ul>       
                            <div class=\"d-flex flex-column align-items-center w-75\" style=\"align-self: center;\">
                                <iframe src=\"https://giphy.com/embed/d3mlE7uhX8KFgEmY\" width=\"480\" height=\"269\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/culture--think-hmm-d3mlE7uhX8KFgEmY\">via GIPHY</a></p>
                            </div>
                        </div>
                    </div>


                    <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
                        <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                            <span class=\"text\">回上一頁</span>
                        </a>
                        <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                            <span class=\"text\">前往課後練習</span>
                        </a>
                    </div>
                    """,
                    "chart_type": None,
                    "chart_config": None,
                    "multi_steps": ["text"]
            }
]

@course3_api.route('/api/course_content/course3')
def get_course3_content():
    return jsonify({"pages": course3_pages})
