import requests
from bs4 import BeautifulSoup
import os
import time

# 定义主页面URL
url = "https://so.gushiwen.cn/gushi/tangshi.aspx"
base_url = "https://so.gushiwen.cn"

# 获取主页面内容
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# 提取诗的链接和类型
poems_links = []
type_conts = soup.find_all('div', class_='typecont')
for type_cont in type_conts:
    poem_type = type_cont.find('div', class_='bookMl').text.strip()
    links = type_cont.find_all('a')
    for link in links:
        poems_links.append((poem_type, base_url + link['href']))

# 定义函数来提取详情页诗的信息
def extract_poem_info(poem_type, poem_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(poem_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 输出调试信息
    print(f"Parsing URL: {poem_url}")
    
    try:
        cont_div = soup.find('div', id=lambda x: x and x.startswith('zhengwen'))
        if not cont_div:
            print(f"Failed to find 'zhengwen' div in {poem_url}")
            return None
        
        title_tag = cont_div.find('h1')
        if not title_tag:
            print(f"Failed to find 'h1' tag in 'zhengwen' div in {poem_url}")
            return None
        title = title_tag.text.strip()
        print(f"Title: {title}")

        source_p = cont_div.find('p', class_='source')
        if not source_p:
            print(f"Failed to find 'source' p tag in {poem_url}")
            return None
        
        author_info = source_p.find_all('a')
        if len(author_info) < 1:
            print(f"Failed to find author info in {poem_url}")
            return None
        
        author = author_info[0].text.strip()
        print(f"Author: {author}")

        content_div = cont_div.find('div', class_='contson')
        if not content_div:
            print(f"Failed to find 'contson' div in {poem_url}")
            return None
        
        content = content_div.text.strip()
        content = content.replace('\n', '').replace('\r', '').replace('\t', '')
        print(f"Content: {content}")

        return f"{poem_type},{title},{content},{author}"
    except Exception as e:
        print(f"Error parsing {poem_url}: {e}")
        return None

# 提取所有诗的信息
poem_data = []
for poem_type, poem_link in poems_links:
    poem_info = extract_poem_info(poem_type, poem_link)
    if poem_info:
        poem_data.append(poem_info)
    time.sleep(1)  

# 将数据保存为txt文件
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'tang_poems.txt')

# 添加字段名称
with open(output_file, 'w', encoding='utf-8') as file:
    file.write("Type,Title,Content,Author\n")
    for poem in poem_data:
        file.write(poem + '\n')

print(f"数据已保存至 {output_file}")
