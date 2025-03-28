import re
import os
from bs4 import BeautifulSoup

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
        # 假設以 .html 結尾的連結是頁面路由
        if href.endswith('.html'):
            # 移除 .html 後綴，轉為 Flask 路由名稱
            route_name = href[:-5]  # 移除 '.html'
            a_tag['href'] = "{{ url_for('" + route_name + "') }}"
            link_count += 1
    print(f"找到並轉換了 {link_count} 個頁面連結")

    if css_count == 0 and js_count == 0 and img_count == 0 and link_count == 0:
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
    
    # 遍歷目錄中的所有檔案
    for filename in os.listdir(current_dir):
        # 檢查是否為 HTML 檔案
        if filename.endswith('.html'):
            html_file_path = os.path.join(current_dir, filename)
            # 直接覆蓋原檔案
            convert_to_flask_static(html_file_path, html_file_path)