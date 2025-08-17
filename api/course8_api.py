from flask import Blueprint, jsonify

course8_api = Blueprint('course8_api', __name__)

# 真實課程資料（可直接編輯，日後可改為資料庫讀取）
course8_pages = [
        {
                "page_index": 0,
                "html_content": """
                <div class=\"m-4 font-large align-self-center\">
                    <h1 class=\"fw-bolder mb-4 mt-2\">KD隨機指標</h1>
                    <ol>
                        <li class=\"fs-5 mb-2\">由 隨機指標 Stochastic Oscillator 演化而來的技術分析工具</li>
                        <li class=\"fs-5 mb-2\">用來判斷股價的 <strong>超買</strong> 或 <strong>超賣</strong> 狀況，幫助我們抓住<strong>買賣時機</strong></li>
                        <li class=\"fs-5 mb-2\">觀察 K、D 值的交叉情況，判斷股價要漲還是要跌</li>
                        <li class =\"fs-5 mb-2\">常見週期設定：9日KD（RSV公式導出）</li>
                        <li class=\"fs-5 mb-2\">常見使用方式：「K上穿D＝黃金交叉」、「K下穿D＝死亡交叉」</li>
                    </ol>
                </div>
                <div id=\"chart-container\" class=\"card shadow mb-4\" style=\"display:flex;\">
                    <div class=\"card-body align-self-center\">
                        <div class=\"chart-area\">
                            <canvas id=\"chart1\" style=\"display: block; height: 320px;\"></canvas>
                        </div>
                    </div>
                    <p class=\"fs-5 mb-4 align-self-center\">你可以操作圖表來更了解KD隨機指標的變化喔～</p>
                </div>
                <div class=\"d-flex justify-content-center mb-5 pr-5\">
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": "chart1",
                "chart_config": None
        },
        {
            "page_index": 1,
            "html_content": """
            <div class=\"m-4 font-large align-self-center\">
                <h1 class=\"fw-bolder mb-4 mt-2\">判斷買賣訊號</h1>
                <p class=\"fs-5 mb-2\">📈黃金交叉 ：</p>
                <ul>
                    <li>➡️當 K 值向上突破 D 值 時，是<strong>買進</strong>訊號</li>
                    <li>➡️代表<strong>買方</strong>力量增強，股價有可能<strong>開始上漲</strong>。</li>
                    <li>➡️就像潮水退去後又開始上漲，市場情緒轉為樂觀。</li>
                </ul>
                <div id=\"text1\" style=\"display:none;\">
                    <p class=\"fs-5 mb-2\">📉死亡交叉 ：</p>
                    <ul>
                        <li>➡️當 K 值向下突破 D 值 時，是<strong>賣出</strong>訊號</li>
                        <li>➡️代表<strong>賣方</strong>力量增強，股價有可能<strong>開始下跌</strong>。</li>
                        <li>➡️就像潮水退去後又開始下跌，市場情緒轉為悲觀。</li>
                    </ul>
                </div>
                <div id=\"text2\" style=\"display:none;\">
                    <p class=\"fs-5 mb-2\">買方🐂：看好股價上漲，買進股票，推動 K 值上升。</p>
                    <p class=\"fs-5 mb-2\">賣方🐻：看空股價，賣出股票，使 K 值下降。</p>
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
            "multi_steps": ["text1", "text2"]
        },
        {
                "page_index": 2,
                "html_content": """
                <div class=\"m-4 font-large align-self-center\">
                    <h1 class=\"fw-bolder mb-4 mt-2 pl-4\">KD指標的優缺點</h1>
                    <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">
                        <li>🟢優點：</li>
                        <ul>
                            <li>容易判斷進出場時機，新手也能快速上手。</li>
                            <li>在震盪行情 (股價上下波動，但區間不大) 中特別有效</li>
                        </ul>
                    </ul>
                    <div id=\"text1\" style=\"display:none;\">
                        <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">
                            <li>🔴缺點：</li>
                            <ul>
                                <li>
                                    在 
                                    <a href=\"#\" id=\"bull-link\" style=\"color: #007bff; text-decoration: underline;\">牛市</a>
                                    或
                                    <a href=\"#\" id=\"bear-link\" style=\"color: #007bff; text-decoration: underline;\">熊市</a>
                                    中容易出現鈍化，例如：
                                </li>
                                <li>➡️股價連漲，但 KD 指標早已超買。</li>
                                <li>➡️股價連跌，但 KD 指標已超賣。</li>
                                <li> 建議搭配其他技術指標，例如 MACD 或 SMA均線提高準確性。</li>
                            </ul>
                        </ul>
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
                "multi_steps": ["text1"]
            },
        {
                "page_index": 3,
                "html_content": """
                <div class=\"m-4 font-large align-self-center\">
                    <h1 class=\"fw-bolder mb-4 mt-2\">何謂「市場鈍化」?</h1>
                    <p class=\"fs-5 mb-2\">在學習 KD 指標 的時候，經常會聽到 「黃金交叉 = 買進訊號」，「死亡交叉 = 賣出訊號」。<br>但有時真的照著交叉訊號操作，為什麼還是會賠錢？<br>這就要提到 <strong>鈍化現象</strong> 了！。</p>
                    <div id=\"text1\" style=\"display:none;\">
                        <p class=\"fs-5 mb-2\">💡定義：</p>
                        <ul>
                            <li>KD 指標進入超買或超賣區後，卻持續維持高檔或低檔，而股價並沒有出現反轉。</li>
                            <li>換句話說：死亡交叉後，股價還在漲、黃金交叉後，股價卻跌不停。</li>
                        </ul>
                    </div>
                    <div id=\"text2\" style=\"display:none;\">
                        <p class=\"fs-5 mb-2\">💡為什麼會發生鈍化？</p>
                        <ul>
                            <li>當市場非常強勢時，KD 指標可能<strong>長期維持在高檔</strong>（80以上），但股價還是<strong>一路漲</strong>。<br>例如：大牛市、熱門股票受到資金追捧。</li>
                            <ul>
                                <li>➡️此時的死亡交叉可能只是<strong>短暫回調</strong>，而不是趨勢反轉。</li>
                            </ul>
                            <li>在空頭市場中，KD 指標可能<strong>長期維持在低檔</strong>（20以下），但股價卻<strong>繼續下跌</strong>。<br>例如：經濟衰退、重大利空消息。</li>
                            <ul>
                                <li>➡️此時的黃金交叉 在這種情況下可能是<strong>下跌中繼</strong>，而非反轉訊號。</li>
                            </ul>
                        </ul>
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
                "multi_steps": ["text1", "text2"]
        },
        {
                "page_index": 4,
                "html_content": """
                <div class=\"m-4 font-large align-self-center\">
                    <h1 class=\"fw-bolder mb-4 mt-2\">何謂「市場鈍化」?</h1>
                    <p class=\"fs-5 mb-4\">📊 舉個例子：</p>
                    <ul class=\"fs-5 mb-4\">
                        <li>假設某支熱門科技股因為新品發表會，大受市場歡迎，投資人瘋狂買進。</li>
                        <li>KD 指標進入超買區，並且出現 死亡交叉。</li>
                        <li>理論上，死亡交叉是賣出訊號，但股價卻因為<strong>強勁的買盤支撐</strong>，繼續上漲。</li>
                    </ul>
                    <p class=\"fs-5 mb-4\">這就是<strong>鈍化現象</strong>，因為市場的買方力量太強，指標失效了。</p>
                    <div id=\"text1\" style=\"display:none;\">
                        <p class=\"fs-5 mb-4\">⚠️ 怎麼應對鈍化現象？</p>
                        <ul class=\"fs-5 mb-4\">
                            <li>不要單單依靠 KD 指標：KD 指標 容易在 <strong>強勢趨勢</strong> 中出現 <strong>鈍化</strong>。<br>建議搭配其他技術指標例如：MACD、SMA均線、成交量。</li>
                            <li>觀察趨勢結構：在 <strong>多頭趨勢</strong> 中，即使死亡交叉也不一定要急著賣出。<br>在 <strong>空頭趨勢</strong> 中，即使黃金交叉也不一定要急著買進。</li>
                        </ul>
                    </div>
                    <div id=\"text2\" style=\"display:none;\">
                        <p class=\"fs-5 mb-4\">簡單總結：</p>
                        <ul class=\"fs-5 mb-4\">
                            <li>鈍化現象 就是 <strong>KD 指標失效</strong> 的情況，通常出現在 <strong>強勢趨勢</strong> 中。</li>
                            <li><strong>死亡交叉</strong> 不一定代表 反轉下跌，有可能只是 回調後繼續上漲。</li>
                            <li><strong>黃金交叉</strong> 也不一定代表 反轉上漲，可能只是 下跌中繼。</li>
                            <li>建議搭配其他指標，並且觀察市場趨勢和成交量，避免被單一指標誤導。</li>
                        </ul>
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
                "multi_steps": ["text1", "text2"]
        },
        {
                "page_index": 5,
                "html_content": """
                <div class=\"m-4 font-large\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">KD隨機指標概念</h2>
                    <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">
                        <li>🟢K 值：反應股價短期波動，屬於快速指標，變化靈敏</li>
                        <li>🟢D 值：K值的移動平均線，屬於穩定訊號，變化較慢</li>
                        <li>🟢數值會介於0~100之間</li>
                    </ul>
                    <ul class=\"fs-5 mb-4\" style=\"list-style-type: none;\">
                        <li>🔵K值高於D值，表示股價偏強勢</li>
                        <li>🔵K值低於D值，表示股價偏弱勢</li>
                    </ul>
                        <img  src=\"/static/images/kd_formula.png\" alt=\"cross types\" style=\"max-width:50vw;\">  
                </div>
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
                "chart_config": None
        },
        {
                "page_index": 6,
                "html_content": """
                <div class=\"m-4 font-large w-75\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">KD指標搭配K線圖解1</h2>
                    <p class=\"fs-5 mb-4\">一、明顯的超買區（KD值 > 80）：</p>
                    <div id=\"chart-container\" class=\"card shadow mb-4\" style=\"display:flex;\">
                        <div class=\"card-body align-self-center\">
                            <div class=\"chart-area\">
                                <canvas id=\"chart2\" style=\"display: block; height: 320px;\"></canvas>
                            </div>
                        </div>
                     <p class=\"fs-5 mb-4 align-self-center\">你可以操作圖表來更了解KD隨機指標的變化喔～</p>
                    </div>
                    <ul class=\"fs-5 mb-4\">
                        <li>
                            <span id=\"stoch-rsi-hover\" style=\"text-decoration:underline; cursor:pointer;\">
                                Stoch RSI的K 線(藍色)與 D 線(橘色) 同時在 90 (紅線)上方
                            </span>
                            <span id=\"stoch-rsi-tooltip\" style=\"display:none; position:absolute; background:#fffbe7; border:1px solid #ccc; padding:8px; border-radius:6px; font-size:1rem; z-index:1000;\">
                                當 Stoch RSI 接近 100，代表市場極度亢奮，我們應該提醒自己別太貪心！
                            </span>
                        </li>
                        <li>說明：</li>
                        <ul class=\"fs-5 mb-4\">
                            <li>此為<strong>超買訊號</strong>，市場情緒非常樂觀。</li>
                            <li>高檔不一定立刻下跌，但風險已經提升。</li>
                        </ul>
                    </ul>
                </div>
                <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": "chart2",
                "chart_config": None
        },
        {
                "page_index": 7,
                "html_content": """
                <div class=\"m-4 font-large w-75\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">KD指標搭配K線圖解2</h2>
                    <p class=\"fs-5 mb-4\">二、超賣區（<20）＋反彈出現：</p>
                    <div id=\"chart-container\" class=\"card shadow mb-4\" style=\"display:flex;\">
                        <div class=\"card-body align-self-center\">
                            <div class=\"chart-area\">
                                <canvas id=\"chart3\" style=\"display: block; height: 320px;\"></canvas>
                            </div>
                        </div>
                     <p class=\"fs-5 mb-4 align-self-center\">你可以操作圖表來更了解KD隨機指標的變化喔～</p>
                    </div>
                    <p class=\"fs-5 mb-4\">約在 6/3～6/13，Stoch RSI 來到 10 以下。</p>
                    <ul class=\"fs-5 mb-4\">
                        <li>說明：</li>
                        <ul class=\"fs-5 mb-4\">
                            <li>市場處於<strong>超賣區</strong>，出現<strong>短線低點</strong>機會。</li>
                            <li>若搭配一根紅K將會是反彈信號。</li>
                        </ul>
                    </ul>
                </div>
                <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">繼續</span>
                    </a>
                </div>
                """,
                "chart_type": "chart3",
                "chart_config": None
        },
            {
                    "page_index": 8,
                    "html_content": """
                    <div class=\"m-4 font-large w-75\" style=\"align-self: center;\">
                        <h2 class=\"fw-bolder mb-4 mt-2\">KD指標搭配K線圖解3</h2>
                        <div id=\"chart-container\" class=\"card shadow mb-4\" style=\"display:flex;\">
                            <div class=\"card-body align-self-center\">
                                <div class=\"chart-area\">
                                    <canvas id=\"chart4\" style=\"display: block; height: 320px;\"></canvas>
                                </div>
                            </div>
                         <p class=\"fs-5 mb-4 align-self-center\">黃金交叉範例：K線上穿D線，出現買進訊號。</p>
                        </div>
                        <ul class=\"fs-5 mb-4\">
                            <li>說明：</li>
                            <ul class=\"fs-5 mb-4\">
                                <li>此為<strong>黃金交叉</strong>，市場情緒轉為樂觀。</li>
                                <li>可搭配成交量觀察是否有主力進場。</li>
                            </ul>
                        </ul>
                    </div>
                    <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
                        <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                            <span class=\"text\">回上一頁</span>
                        </a>
                        <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                            <span class=\"text\">繼續</span>
                        </a>
                    </div>
                    """,
                    "chart_type": "chart4",
                    "chart_config": None
            },
            {
                "page_index": 9,
                "html_content": """
                <div class=\"m-4 font-large w-75\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">KD指標搭配K線圖解4</h2>
                    <div id=\"chart-container\" class=\"card shadow mb-4\" style=\"display:flex;\">
                        <div class=\"card-body align-self-center\">
                            <div class=\"chart-area\">
                                <canvas id=\"chart5\" style=\"display: block; height: 320px;\"></canvas>
                            </div>
                        </div>
                     <p class=\"fs-5 mb-4 align-self-center\">懸崖式高檔死亡交叉範例：K線下穿D線，出現賣出訊號。</p>
                    </div>
                    <ul class=\"fs-5 mb-4\">
                        <li>說明：</li>
                        <ul class=\"fs-5 mb-4\">
                            <li>此為<strong>死亡交叉</strong>，市場情緒轉為悲觀。</li>
                            <li>可搭配成交量觀察是否有主力出貨。</li>
                        </ul>
                    </ul>
                </div>
                <div class=\"d-flex mb-5 justify-content-center\" style=\"gap: 10%\">
                    <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
                        <span class=\"text\">回上一頁</span>
                    </a>
                    <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
                        <span class=\"text\">完成</span>
                    </a>
                </div>
                """,
                "chart_type": "chart5",
                "chart_config": None
            },
            {
                "page_index": 10,
                "html_content": """
                <div class=\"m-4 font-large w-75\" style=\"align-self: center;\">
                    <h2 class=\"fw-bolder mb-4 mt-2\">KD指標課程總結</h2>
                    <ul class=\"fs-5 mb-4\">
                        <li>KD指標是判斷超買超賣、買賣時機的好工具，但要搭配其他指標與市場趨勢。</li>
                        <li>黃金交叉、死亡交叉不是絕對，鈍化現象需特別留意。</li>
                        <li>多練習、觀察不同情境，才能靈活運用KD指標。</li>
                    </ul>
                    <p class=\"fs-5 mb-4\">恭喜你完成第八課！可以進行練習或回到課程選單。</p>
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
                "chart_config": None
            },
]

@course8_api.route('/api/course_content/course8')
def get_course8_content():
    return jsonify({"pages": course8_pages})
