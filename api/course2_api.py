from flask import Blueprint, jsonify
import pymysql
import json

course2_api = Blueprint('course2_api', __name__)

# 課程2資料（可直接編輯，日後可改為資料庫讀取）
# course2_pages = [
#         {
#                 "page_index": 0,
#                 "html_content": """
#                 <div class=\"d-flex flex-column m-4 font-large align-self-center\">
#                     <h1 class=\"fw-bolder mb-4 mt-2\">基本面分析是什麼?</h1>
#                     <p class=\"fs-5 mb-4\">有人說，掌握基本面分析就能看透一家公司內在的價值，甚至找到投資的黃金機會？</p>
#                     <p class=\"fs-5 mb-4\">其實，它是一種幫助我們透過財報數據與經營指標，了解企業真實狀況的工具。</p>
#                     <img src=\"https://a.c-dn.net/c/content/dam/publicsites/aum-cn/images/marketanalysis/what_is_technical_analysis.png/jcr:content/renditions/original-size.webp\" alt=\"基本面分析圖示\" class=\"img-fluid mb-4\">
#                     <p class=\"mt-4 text-muted medium\" style=\"text-align:center;\">
#                         圖片來源：<a href=\"https://www.ig.com/cn/trading-strategies/beginners-guide-to-fundamental-analysis-230414\" target=_blank>
#                                 基本面分析什麼？如何使用基本面分析？
#                         </a>
#                     </p> 
#                 </div>
#                 <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                         <span class=\"text\">回上一頁</span>
#                     </a>
#                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                         <span class=\"text\">繼續</span>
#                     </a>
#                 </div>
#                 """,
#                 "chart_type": None,
#                 "chart_config": None
#         },
#         {
#                 "page_index": 1,
#                 "html_content": """
#                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                 <h1 class=\"fw-bolder mb-4 mt-2\">基本面分析是什麼?</h1>
#                 <p class=\"fs-5 mb-4\">當你在評估一家公司的時候，除了觀察其股價波動，更重要的是瞭解其內在價值。</p>
#                 <p class=\"fs-5 mb-4\">基本面分析就像是一場全面的健康檢查！</p>
#                     <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                     <iframe src=\"https://giphy.com/embed/Y2wwz20Ji8N4DrnGFJ\" width=\"300rem\" height=\"300rem\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe>
#                     <p><a href=\"https://giphy.com/gifs/pudgypenguins-explain-explaining-analysis-Y2wwz20Ji8N4DrnGFJ\">via GIPHY</a></p>
#                 </div>
#                 <p class=\"fs-5 mb-4\" style=\"text-align:center;\">📚本課程將引導你從獲利、經營、安全與價值四大面向來介紹。</p>
#             </div>
#             <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                 <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                     <span class=\"text\">回上一頁</span>
#                 </a>
#                 <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                     <span class=\"text\">繼續</span>        
#                 </a>
#             </div>
#                 """,
#                 "chart_type": None,
#                 "chart_config": None
#         },
#         {
#                 "page_index": 2,
#                 "html_content": """
#                 <div class=\"m-4 font-large align-self-center d-flex flex-column align-items-center\">
#                     <h1 class=\"fw-bolder mb-4 mt-2\">一、獲利性分析：評估公司的賺錢能力</h1>
#                     <p class=\"fs-5 mb-4\">著重於衡量公司從業務活動中創造獲利的能力，類似於檢查一個人的體能狀況，確定其日常表現是否足夠出色！</p>
#                     <img src=\"https://blog.fugle.tw/wp-content/uploads/2020/11/image1-768x433.png\" alt=\"獲利性分析圖示\" class=\"img-fluid mb-4\" style=\"text-align:center;\">
#                     <p class=\"mt-4 text-muted medium\" style=\"text-align:center;\">
#                         圖片來源：<a href=\"https://blog.fugle.tw/quant-pass-financial-index/\" target=_blank>
#                                 【量化通專欄】看財務指標＝基本面投資？太膚淺囉！
#                         </a>
#                     </p> 
#                 </div>
#                 <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                         <span class=\"text\">回上一頁</span>
#                     </a>
#                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                         <span class=\"text\">繼續</span>
#                     </a>
#                 </div>
#                 """,
#                 "chart_type": None,
#                 "chart_config": None
#         },
#         {
#                 "page_index": 3,
#                 "html_content": """
#                 <div class=\"m-4 font-large\" style=\"align-self: center;\">
#                     <h2 class=\"fw-bolder mb-4 mt-2\">一、獲利性分析：評估公司的賺錢能力</h2>
#                 </div>
#                 <div class=\"card-body\">
#                     <div class=\"table-responsive\">
#                         <table class=\"table table-bordered\">
#                             <tbody>
#                                 <tr>
#                                     <th style=\"vertical-align:middle;\">毛利率</th>
#                                     <td>
#                                         <ul style=\"margin:0; padding:1rem;\">
#                                             <li>衡量銷售收入扣除直接成本後的利潤</li>
#                                             <li>反映產品或服務的基本獲利能力。</li>
#                                         </ul>
#                                     </td>
#                                 </tr>
#                                 <tr>
#                                     <th>營業利益率</th>
#                                     <td>剖析營運效率，告訴你公司在扣除營運成本後的盈餘狀況。</td>
#                                 </tr>
#                                 <tr>
#                                     <th>淨利率</th>
#                                     <td>最終獲利能力的展示，反映公司扣除所有費用、稅項後的淨收益。</td>
#                                 </tr>
#                                 <tr>
#                                     <th>股東權益報酬率（ROE）</th>
#                                     <td>評估股東投資的回報率，類似檢視投資「健康指數」。</td>
#                                 </tr>
#                                 <tr>
#                                     <th>總資產報酬率（ROA）</th>
#                                     <td>衡量公司利用全部資產創造收益的效率。</td>
#                                 </tr>
#                                 <tr>
#                                     <th>每股盈餘（EPS）</th>
#                                     <td>代表每一股股票帶來的實際利潤，供投資人直接參考。</td>
#                                 </tr>
#                                 <tr>
#                                     <th>獲利含金量</th>
#                                     <td>綜合考量毛利、營業利潤與其他成本，判斷獲利質量是否穩固。</td>
#                                 </tr>
#                             </tbody>
#                         </table>
#                         </div>
#                 </div>
#                 <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                         <span class=\"text\">回上一頁</span>
#                     </a>
#                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                         <span class=\"text\">繼續</span>
#                     </a>
#                 </div>
#                 """,
#                 "chart_type": None,
#                 "chart_config": None
#         },
#         {
#                 "page_index": 4,
#                 "html_content": """
#                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                 <h1 class=\"fw-bolder mb-4 mt-2\">一、獲利性分析：評估公司的賺錢能力</h1>
#                 <p class=\"fs-5 mb-4\">📊實例應用：</p>
#                 <p class=\"fs-5 mb-4\">想像一家餐廳，毛利率就像是菜品定價與原料成本的差額；營業利益率則是廚師效率與服務水平的綜合體現；而ROE則代表餐廳投資回報的高低。</p>
#                 <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                     <iframe src=\"https://giphy.com/embed/rXfM5oNgqENj2\" width=\"480\" height=\"360\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/restaurant-rXfM5oNgqENj2\">via GIPHY</a></p>
#                 </div>
#         </div>
#             <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                 <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                     <span class=\"text\">回上一頁</span>
#                 </a>
#                 <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                     <span class=\"text\">繼續</span>
#                 </a>
#             </div>
#                 """,
#                 "chart_type": None,
#                 "chart_config": None
#                 },
#                 {
#                         "page_index": 5,
#                         "html_content": """
#                         <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                             <h1 class=\"fw-bolder mb-4 mt-2\">一、獲利性分析：評估公司的賺錢能力</h1>
#                             <p class=\"fs-5 mb-4\">📊真實案例：</p>
#                             <p class=\"fs-5 mb-4\">以蘋果公司為例，2020年的毛利率約在38%左右，營業利益率與淨利率也維持在業界領先水準，再加上穩定的ROE（通常超過20%），使得投資人能夠清楚看出其強勁的獲利能力。</p>
#                             <img src=\"https://s.wsj.net/public/resources/images/S1-FX287_apple0_OR_20200430175116.jpg\" alt=\"基本面分析圖示\" class=\"img-fluid mb-4\">
#                             <p class=\"mt-4 text-muted medium\" style=\"text-align:center;\">
#                                 圖片來源：<a href=\"https://cn.wsj.com/articles/蘋果公司銷售額小幅增長，在疫情中展現韌性-11588289412\" target=_blank>
#                                         蘋果公司銷售額小幅增長，在疫情中展現韌性
#                                 </a>
#                             </p> 
#                         </div>
#                         <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                 <span class=\"text\">回上一頁</span>
#                             </a>
#                             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                 <span class=\"text\">繼續</span>
#                             </a>
#                         </div>
#                         """,
#                         "chart_type": None,
#                         "chart_config": None
#                 },
#                 {
#                         "page_index": 6,
#                         "html_content": """
#                         <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                 <h1 class=\"fw-bolder mb-4 mt-2\">二、經營力分析：檢視資源運用與管理效率</h1>
#                                 <p class=\"fs-5 mb-4\">經營力分析關注公司如何有效利用資源創造營收，就像評估一位運動員如何高效運用自己的體能與技術，完成比賽。</p>
#                                 <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                                     <iframe src=\"https://giphy.com/embed/y55SYeCKDybLzJ4jsF\" width=\"480rem\" height=\"259rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/news-running-tired-skip-y55SYeCKDybLzJ4jsF\">via GIPHY</a></p>
#                                 </div>
#                             </div>
#                             <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                                 <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                     <span class=\"text\">回上一頁</span>
#                                 </a>
#                                 <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                     <span class=\"text\">繼續</span>
#                                 </a>
#                             </div>
#                         """,
#                         "chart_type": None,
#                         "chart_config": None
#                 },
#                 {
#                         "page_index": 7,
#                         "html_content": """
#                         <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                             <h2 class=\"fw-bolder mb-4 mt-2\">二、經營力分析：檢視資源運用與管理效率</h2>
#                         </div>
#                         <div class=\"card-body\">
#                             <div class=\"table-responsive\">
#                                 <table class=\"table table-bordered\">
#                                     <tbody>
#                                         <tr>
#                                             <th style=\"vertical-align:middle;\">總資產週轉率</th>
#                                             <td>衡量公司利用所有資產產生銷售收入的效率，反映資產配置是否合理。</td>
#                                         </tr>
#                                         <tr>
#                                             <th>應收帳款週轉率</th>
#                                             <td>揭示公司收回銷售款項的速度，類似評估現金流入的「反應速度」。</td>
#                                         </tr>
#                                         <tr>
#                                             <th>存貨週轉率</th>
#                                             <td>展示存貨管理效率，確保資源不被過多囤積，保持營運靈活性。</td>
#                                         </tr>
#                                     </tbody>
#                                 </table>
#                                 </div>
#                         </div>
#                         <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#                             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                 <span class=\"text\">回上一頁</span>
#                             </a>
#                             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                 <span class=\"text\">繼續</span>
#                             </a>
#                         </div>
#                         """,
#                         "chart_type": None,
#                         "chart_config": None
#                 },
#                 {
#                         "page_index": 8,
#                         "html_content": """
#                         <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                             <h1 class=\"fw-bolder mb-4 mt-2\">二、經營力分析：檢視資源運用與管理效率</h1>
#                             <p class=\"fs-5 mb-4\">📊實例應用：</p>
#                             <ul class=\"fs-5 mb-4\">
#                                 <li>把公司比作一台高效運轉的機器，總資產週轉率就是機器的生產效率</li>
#                                 <li>應收帳款與存貨週轉率則分別代表原料進貨與產品出庫的流暢度</li>
#                                 <li>管理得當意味著企業能迅速將投入轉化為現金與利潤</li>
#                             </ul>
#                             <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                                     <iframe src=\"https://giphy.com/embed/lyxIb7MBfv14I\" width=\"480rem\" height=\"317rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/hateplow-work-forever-hateplow-lyxIb7MBfv14I\">via GIPHY</a></p>
#                             </div>
#                         </div>
#                         <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                 <span class=\"text\">回上一頁</span>
#                             </a>
#                             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                 <span class=\"text\">繼續</span>
#                             </a>
#                         </div>
#                         """,
#                         "chart_type": None,
#                         "chart_config": None
#                 },
#                 {
#                         "page_index": 9,
#                         "html_content": """
#                         <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                             <h2 class=\"fw-bolder mb-4 mt-2\">二、經營力分析：檢視資源運用與管理效率</h2>
#                             <p class=\"fs-5 mb-4\">📊真實案例：</p>
#                             <ul class=\"fs-5 mb-4\">
#                                 <li>以台積電為例，該公司在全球半導體產業中以高效的生產與供應鏈管理著稱</li>
#                                 <li>台積電的總資產週轉率雖不會非常高（因資產龐大），但其應收帳款與存貨管理均十分出色，這使得公司能快速將資源轉化為銷售收入，進而提升整體營運效率。</li>
#                             </ul>
#                             <img src=\"https://ibw.bwnet.com.tw/ac_gallery/2020/11/ca8b3597-4d6a-f361-f5af-782eaa9f07d4_800.webp\" alt=\"基本面分析圖示\" class=\"img-fluid mb-4\">
#                             <p class=\"mt-4 text-muted medium\" style=\"text-align:center;\">
#                                 圖片來源：<a href=\"https://www.businessweekly.com.tw/management/blog/3004655\" target=_blank>
#                                         除了高薪高壓，「台積電員工」有哪些DNA？6原則，看懂護國神山經營力
#                                 </a>
#                             </p> 
#                         </div>

#                         <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                             <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                 <span class=\"text\">回上一頁</span>
#                             </a>
#                             <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                 <span class=\"text\">繼續</span>
#                             </a>
#                         </div>
#                         """,
#                         "chart_type": None,
#                         "chart_config": None
#                         },
#                         {
#                                 "page_index": 10,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h1 class=\"fw-bolder mb-4 mt-2\">三、安全性分析：評估公司的財務穩健度</h1>
#                                     <p class=\"fs-5 mb-4\">安全性分析就像是對公司進行一場財務健康檢查，確保公司在面對市場波動或突發狀況時，有足夠的資金與資源應對挑戰。</p>
#                                     <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                                         <iframe src=\"https://giphy.com/embed/3o6MblsoRCn3wFRKxy\" width=\"480rem\" height=\"360rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/season-12-the-simpsons-12x9-3o6MblsoRCn3wFRKxy\">via GIPHY</a></p>
#                                     </div>
#                                 </div>
#                                 <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">繼續</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         },
#                         {
#                                 "page_index": 11,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h2 class=\"fw-bolder mb-4 mt-2\">三、安全性分析：評估公司的財務穩健度</h2>
#                                 </div>
#                                 <div class=\"card-body\">
#                                     <div class=\"table-responsive\">
#                                         <table class=\"table table-bordered\">
#                                             <tbody>
#                                                 <tr>
#                                                     <th style=\"vertical-align:middle;\">流動比率</th>
#                                                     <td>衡量公司短期資產對短期負債的覆蓋能力，確保日常運營不致資金斷裂。</td>
#                                                 </tr>
#                                                 <tr>
#                                                     <th>速動比率</th>
#                                                     <td>進一步剔除存貨因素，更嚴格地評估公司快速變現能力。</td>
#                                                 </tr>
#                                                 <tr>
#                                                     <th>自由現金流</th>
#                                                     <td>扣除必要支出後，真正可以自由支配的現金量，象徵企業的經濟後盾與彈性。</td>
#                                                 </tr>
#                                             </tbody>
#                                         </table>
#                                         </div>
#                                 </div>
#                                 <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">繼續</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         },
#                         {
#                                 "page_index": 12,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h1 class=\"fw-bolder mb-4 mt-2\">三、安全性分析：評估公司的財務穩健度</h1>
#                                     <p class=\"fs-5 mb-4\">📊實例應用：</p>
#                                     <p class=\"fs-5 mb-4\"> 就好比個人理財，你需要確保銀行帳戶中有足夠的流動資金應對突發狀況；同理，企業擁有充裕的自由現金流，就能在市場低迷時進行調整或抓住突發機遇。</p>
#                                     <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                                         <iframe src=\"https://giphy.com/embed/aoZNck1kze91pNwLex\" width=\"480rem\" height=\"480rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/money-rich-dollar-aoZNck1kze91pNwLex\">via GIPHY</a></p>
#                                     </div>
#                                 </div>
#                                 <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">繼續</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         },
#                         {
#                                 "page_index": 13,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h1 class=\"fw-bolder mb-4 mt-2\">三、安全性分析：評估公司的財務穩健度</h1>
#                                     <p class=\"fs-5 mb-4\">📊真實案例：</p>
#                                     <p class=\"fs-5 mb-4\"> 以亞馬遜為例，儘管其在擴張期間進行了大量投資，但公司仍持續保持較高的自由現金流與合理的流動比率，這使得亞馬遜在面對市場不確定性時能夠迅速調整策略，並抓住新興市場機會。</p>
#                                     <img src=\"https://ibw.bwnet.com.tw/ac_gallery/2021/02/6ab948dc-3a1a-e1b3-9738-2ec5a403682c_800.webp\" alt=\"基本面分析圖示\" class=\"img-fluid mb-4\">
#                                     <p class=\"mt-4 text-muted medium\" style=\"text-align:center;\">
#                                         圖片來源：<a href=\"https://www.businessweekly.com.tw/business/blog/3005449\" target=_blank>
#                                                 超乎預期！亞馬遜一季營收3.5兆，最強的獲利武器不是「萬貨電商」
#                                         </a>
#                                     </p> 
#                                     </div>
#                                 <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">繼續</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         },
#                         {
#                                 "page_index": 14,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h1 class=\"fw-bolder mb-4 mt-2\">四、價值性分析：判斷股票的合理定價</h1>
#                                     <p class=\"fs-5 mb-4\">價值性分析主要幫助投資人判斷一隻股票是否被市場低估或高估，就像消費者在購買商品時會考慮性價比，確保花的每一分錢都值得。</p>
#                                     <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                                         <iframe src=\"https://giphy.com/embed/G4qAZYIFr1Cww\" width=\"480rem\" height=\"317rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/cat-paw-coin-G4qAZYIFr1Cww\">via GIPHY</a></p>
#                                     </div>
#                                 </div>
#                                 <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">繼續</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         },
#                         {
#                                 "page_index": 15,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h2 class=\"fw-bolder mb-4 mt-2\">四、價值性分析：判斷股票的合理定價</h2>
#                                 </div>
#                                 <div class=\"card-body\">
#                                     <div class=\"table-responsive\">
#                                         <table class=\"table table-bordered\">
#                                             <tbody>
#                                                 <tr>
#                                                     <th style=\"vertical-align:middle;\">本益比（PE）</th>
#                                                     <td>最常用的估值工具，反映股價相對於每股盈餘的倍數。</td>
#                                                 </tr>
#                                                 <tr>
#                                                     <th>股價淨值比（PBR）</th>
#                                                     <td>以公司帳面價值衡量股價是否合理，考慮企業資產保值能力。</td>
#                                                 </tr>
#                                                 <tr>
#                                                     <th>現金殖利率</th>
#                                                     <td>展示投資人從股息中獲得的現金回報，類似於「紅利」的實際收益。</td>
#                                                 </tr>
#                                             </tbody>
#                                         </table>
#                                         </div>
#                                 </div>
#                                 <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">繼續</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         },
#                         {
#                                 "page_index": 16,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h1 class=\"fw-bolder mb-4 mt-2\">四、價值性分析：判斷股票的合理定價</h1>
#                                     <p class=\"fs-5 mb-4\">📊實例應用：</p>
#                                     <p class=\"fs-5 mb-4\">想像你在購物，PE 就像是衡量產品價格與品質之間的關係；PBR 則告訴你這個品牌的實際價值，而現金殖利率則相當於購買後享受到的現金回饋。</p>
#                                     <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                                         <iframe src=\"https://giphy.com/embed/WfaHuht7D5SSNfetTf\" width=\"480rem\" height=\"269rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/usagi-chiikawa-hachiware-WfaHuht7D5SSNfetTf\">via GIPHY</a></p>
#                                     </div>
#                                 </div>
#                                 <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">繼續</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         },
#                         {
#                                 "page_index": 17,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h2 class=\"fw-bolder mb-4 mt-2\">四、價值性分析：判斷股票的合理定價</h2>
#                                     <p class=\"fs-5 mb-4\"> 📊真實案例：</p>
#                                     <ul class=\"fs-5 mb-4\">
#                                         <li>以台積電為例，其本益比與股價淨值比常被拿來與國際同業比較。投資人可以透過這些指標，評估台積電在市場中的定價是否合理，進而判斷是否具備長期投資價值。</li>
#                                         <li>同時，穩定的股息政策也使得現金殖利率成為衡量其投資吸引力的一個重要參考。</li>
#                                     </ul>
#                                     <img src=\"https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2024/10/09/realtime/30685777.jpg\" alt=\"基本面分析圖示\" class=\"img-fluid mb-4\">
#                                     <p class=\"mt-4 text-muted medium\" style=\"text-align:center;\">
#                                         圖片來源：<a href=\"https://udn.com/news/story/7251/8284079\" target=_blank>
#                                             台積法說 台股推演三情境
#                                         </a>
#                                     </p> 
#                                 </div>

#                                 <div class=\"d-flex justify-content-center\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">繼續</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         },
#                         {
#                                 "page_index": 18,
#                                 "html_content": """
#                                 <div class=\"d-flex flex-column m-4 font-large align-self-center w-100\" style=\"max-width: 600px; margin: 0 auto; overflow-x: auto; overflow-y: auto;\">
#                                     <h1 class=\"fw-bolder mb-4 mt-2\">📊課程回顧，為什麼要學習基本面分析？</h1>
#                                     <p class=\"fs-5 mb-4\">了解公司內在： 從數據中洞察公司經營的真實情況，不被短期市場波動干擾。</p>
#                                     <p class=\"fs-5 mb-4\">降低投資風險： 透過財務健康檢查，幫助你選擇更穩健的投資標的。</p>
#                                     <p class=\"fs-5 mb-4\">提升決策精準度： 結合多項指標，進行綜合判斷，讓你的投資決策更有依據，就像醫生根據全方位檢查結果給出診斷建議一樣。</p>
#                                     <div class=\"d-flex flex-column align-items-center w-100\" style=\"align-self: center;\">
#                                         <iframe src=\"https://giphy.com/embed/kKtAJrJUQnuikFZr3c\" width=\"480rem\" height=\"360rem\" style=\"\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"https://giphy.com/gifs/chiikawa-kKtAJrJUQnuikFZr3c\">via GIPHY</a></p>
#                                     </div>
#                                 </div>
#                                 <div class=\"d-flex justify-content-center mb-5\" style=\"gap: 10%\">
#                                     <a href=\"#\" class=\"btn btn-dark btn-icon-split w-10 align-self-center\" id=\"prev-btn\">
#                                         <span class=\"text\">回上一頁</span>
#                                     </a>
#                                     <a href=\"#\" class=\"btn btn-info btn-icon-split w-10 align-self-center\" id=\"continue-btn\">
#                                         <span class=\"text\">前往課後練習</span>
#                                     </a>
#                                 </div>
#                                 """,
#                                 "chart_type": None,
#                                 "chart_config": None
#                         }
# ]

@course2_api.route('/api/course_content/course2')
def get_course2_content():
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
        "FROM course_pages WHERE course_id=%s ORDER BY page_index", ('course2',)
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
