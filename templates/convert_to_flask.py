import re
import os
from bs4 import BeautifulSoup

def convert_js_file(js_file, output_file=None):
    """
    將 JavaScript 檔案中的 HTML 連結轉換為 Flask 路由格式。
    
    :param js_file: 輸入的 JS 檔案路徑
    :param output_file: 輸出的 JS 檔案路徑（預設覆蓋原檔案）
    """
    if output_file is None:
        output_file = js_file

    print(f"正在處理 JS 檔案：{js_file}")

    try:
        with open(js_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"無法讀取檔案 {js_file}：{e}")
        return

    original_content = js_content
    
    # 處理 window.location.href="practice數字.html" -> window.location.href="/practice數字"
    js_content = re.sub(
        r'window\.location\.href\s*=\s*["\'](?:\.\/)?practice(\d+)\.html(?:\?[^"\']*)?["\']',
        r'window.location.href="/practice\1"',
        js_content
    )
    
    # 處理 window.location.href="course數字.html" -> window.location.href="/course數字"
    js_content = re.sub(
        r'window\.location\.href\s*=\s*["\'](?:\.\/)?course(\d+)\.html(?:\?[^"\']*)?["\']',
        r'window.location.href="/course\1"',
        js_content
    )
    
    # 處理一般的 practice數字.html -> /practice數字
    js_content = re.sub(
        r'["\'](?:\.\/)?practice(\d+)\.html(?:\?[^"\']*)?["\']',
        r'"/practice\1"',
        js_content
    )
    
    # 處理一般的 course數字.html -> /course數字
    js_content = re.sub(
        r'["\'](?:\.\/)?course(\d+)\.html(?:\?[^"\']*)?["\']',
        r'"/course\1"',
        js_content
    )
    
    # 處理 href 屬性中的 course數字.html
    js_content = re.sub(
        r'href\s*=\s*["\'](?:\.\/)?course(\d+)\.html(?:\?[^"\']*)?["\']',
        r'href="/course\1"',
        js_content
    )
    
    # 處理 href 屬性中的 practice數字.html
    js_content = re.sub(
        r'href\s*=\s*["\'](?:\.\/)?practice(\d+)\.html(?:\?[^"\']*)?["\']',
        r'href="/practice\1"',
        js_content
    )
    
    if js_content != original_content:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(js_content)
            print(f"轉換完成，已覆蓋檔案：{output_file}")
        except Exception as e:
            print(f"無法寫入檔案 {output_file}：{e}")
    else:
        print("沒有找到需要轉換的連結")

def convert_to_flask_static(html_file, output_file=None):
    """
    將 HTML 文件中的靜態資源和連結轉換為 Flask 的 url_for 格式。
    
    :param html_file: 輸入的 HTML 檔案路徑
    :param output_file: 輸出的 HTML 檔案路徑（預設覆蓋原檔案）
    """
    if output_file is None:
        output_file = html_file

    print(f"正在處理檔案：{html_file}")

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"無法讀取檔案 {html_file}：{e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    # 處理 CSS 文件（<link> 標籤）
    css_count = 0
    for link in soup.find_all('link', href=True):
        href = link['href']
        if href.startswith(('http://', 'https://', '{{')):
            continue
        link['href'] = "{{ url_for('static', filename='" + href.lstrip('./') + "') }}"
        css_count += 1
    print(f"找到並轉換了 {css_count} 個 CSS 引用")

    # 處理 JS 文件（<script> 標籤）
    js_count = 0
    for script in soup.find_all('script', src=True):
        src = script['src']
        if src.startswith(('http://', 'https://', '/cdn-cgi/', '{{')):
            continue
        script['src'] = "{{ url_for('static', filename='" + src.lstrip('./') + "') }}"
        js_count += 1
    print(f"找到並轉換了 {js_count} 個 JS 引用")

    # 處理圖片文件（<img> 標籤）
    img_count = 0
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src.startswith(('http://', 'https://', '{{')):
            continue
        img['src'] = "{{ url_for('static', filename='" + src.lstrip('./') + "') }}"
        img_count += 1
    print(f"找到並轉換了 {img_count} 個圖片引用")

    # 處理頁面連結（<a> 標籤）
    link_count = 0
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # 跳過外部連結、已轉換的 Flask 格式或特殊連結
        if href.startswith(('http://', 'https://', '#', '{{', '/')):
            continue
        
        # 特別處理 course數字.html 連結 (支援任何數字)
        course_match = re.match(r'(?:\.\/)?course(\d+)\.html(?:\?[^"\']*)?', href)
        if course_match:
            course_num = course_match.group(1)
            a_tag['href'] = f"/course{course_num}"
            link_count += 1
            continue
            
        # 特別處理 practice數字.html 連結 (支援任何數字)
        practice_match = re.match(r'(?:\.\/)?practice(\d+)\.html(?:\?[^"\']*)?', href)
        if practice_match:
            practice_num = practice_match.group(1)
            a_tag['href'] = f"/practice{practice_num}"
            link_count += 1
            continue
        
        # 假設以 .html 結尾的連結是頁面路由
        if href.endswith('.html'):
            # 移除 .html 後綴，轉為 Flask 路由名稱
            route_name = href.lstrip('./')[:-5]  # 移除 './' 和 '.html'
            a_tag['href'] = "{{ url_for('" + route_name + "') }}"
            link_count += 1
    print(f"找到並轉換了 {link_count} 個頁面連結")

    # 處理 JavaScript 中的連結
    js_href_count = 0
    for script in soup.find_all('script'):
        if script.string:
            js_content = script.string
            
            # 處理 window.location.href="practice數字.html" -> window.location.href="/practice數字"
            js_content = re.sub(
                r'window\.location\.href\s*=\s*["\'](?:\.\/)?practice(\d+)\.html(?:\?[^"\']*)?["\']',
                r'window.location.href="/practice\1"',
                js_content
            )
            
            # 處理 window.location.href="course數字.html" -> window.location.href="/course數字"
            js_content = re.sub(
                r'window\.location\.href\s*=\s*["\'](?:\.\/)?course(\d+)\.html(?:\?[^"\']*)?["\']',
                r'window.location.href="/course\1"',
                js_content
            )
            
            # 處理一般的 practice數字.html -> /practice數字
            js_content = re.sub(
                r'["\'](?:\.\/)?practice(\d+)\.html(?:\?[^"\']*)?["\']',
                r'"/practice\1"',
                js_content
            )
            
            # 處理一般的 course數字.html -> /course數字
            js_content = re.sub(
                r'["\'](?:\.\/)?course(\d+)\.html(?:\?[^"\']*)?["\']',
                r'"/course\1"',
                js_content
            )
            
            # 處理 href 屬性中的 course數字.html
            js_content = re.sub(
                r'href\s*=\s*["\'](?:\.\/)?course(\d+)\.html(?:\?[^"\']*)?["\']',
                r'href="/course\1"',
                js_content
            )
            
            # 處理 href 屬性中的 practice數字.html
            js_content = re.sub(
                r'href\s*=\s*["\'](?:\.\/)?practice(\d+)\.html(?:\?[^"\']*)?["\']',
                r'href="/practice\1"',
                js_content
            )
            
            if js_content != script.string:
                script.string = js_content
                js_href_count += 1
    
    print(f"找到並轉換了 {js_href_count} 個 JavaScript 連結")

    if css_count == 0 and js_count == 0 and img_count == 0 and link_count == 0 and js_href_count == 0:
        print("沒有找到需要轉換的資源或連結")
        return

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"轉換完成，已覆蓋檔案：{output_file}")
    except Exception as e:
        print(f"無法寫入檔案 {output_file}：{e}")

# 遍歷當前目錄下的所有 HTML 檔案並轉換
if __name__ == "__main__":
    # 獲取當前目錄
    current_dir = os.getcwd()
    
    print("=== 處理 HTML 檔案 ===")
    # 遍歷目錄中的所有檔案
    html_files_found = False
    for filename in os.listdir(current_dir):
        # 檢查是否為 HTML 檔案
        if filename.endswith('.html'):
            html_files_found = True
            html_file_path = os.path.join(current_dir, filename)
            # 直接覆蓋原檔案
            convert_to_flask_static(html_file_path, html_file_path)
    
    if not html_files_found:
        print("沒有找到 HTML 檔案")
    
    print("\n=== 處理 JavaScript 檔案 ===")
    # 檢查 static/js 目錄 (相對於 backend 目錄)
    backend_dir = os.path.dirname(current_dir)  # 從 templates 回到 backend
    static_js_dir = os.path.join(backend_dir, 'static', 'js')
    if os.path.exists(static_js_dir):
        js_files_found = False
        for filename in os.listdir(static_js_dir):
            # 檢查是否為 course1-9.bundle.js、practice1-9.bundle.js、course_selection.bundle.js 或 practice_selection.bundle.js
            if (re.match(r'^(course|practice)[1-9]\.bundle\.js$', filename) or 
                filename in ['course_selection.bundle.js', 'practice_selection.bundle.js']):
                js_files_found = True
                js_file_path = os.path.join(static_js_dir, filename)
                convert_js_file(js_file_path, js_file_path)
        
        if not js_files_found:
            print("沒有找到 course1-9.bundle.js、practice1-9.bundle.js、course_selection.bundle.js 或 practice_selection.bundle.js 檔案")
    else:
        print(f"static/js 目錄不存在：{static_js_dir}")
    
    print("\n轉換完成！")
