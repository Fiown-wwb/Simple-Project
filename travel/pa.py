from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver

def parse_page(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sight_list = soup.find_all('div', class_='_39IWXatdWDBeX-dBcPkTnh')
    data = []
    for sight in sight_list:
        # 获取景区名称
        name_tag = sight.find('a')
        name = name_tag.text if name_tag else 'N/A'
        # 获取热度
        heat_tag = sight.find('span', class_='_2-f9WAzGqSB1X8OjQnCsaD')
        heat = heat_tag.text if heat_tag else 'N/A'
        # 获取评分
        score_tag = sight.find('span', class_='_2nX2IUMtjcHyj2bbI23aXV _3DJ_Ng1rSYx19hPf71hW-1')
        score = score_tag.text if score_tag else 'N/A'
        # 获取价格
        price_tag = sight.find('span', class_='XmpwEB8BYwS0XLn6J1dMl')
        price = price_tag.text if price_tag else 'N/A'
        # 获取位置
        location_tag = sight.find_all('span', class_='_3CIR0seeyY8j14XCMZj1jz')[0] if sight.find_all('span', class_='_3CIR0seeyY8j14XCMZj1jz') else None
        location = location_tag.text if location_tag else 'N/A'
        # 获取评论数
        reviews_tag = sight.find_all('span', class_='_2nX2IUMtjcHyj2bbI23aXV')[-1] if sight.find_all('span', class_='_2nX2IUMtjcHyj2bbI23aXV') else None
        reviews = reviews_tag.text if reviews_tag else 'N/A'
        # 获取距市中心距离
        distance_tag = sight.find_all('span', class_='_3CIR0seeyY8j14XCMZj1jz')[-1] if sight.find_all('span', class_='_3CIR0seeyY8j14XCMZj1jz') else None
        distance = distance_tag.text if distance_tag else 'N/A'
        data.append([name, heat, score, price, location, reviews, distance])
        print([name, heat, score, price, location, reviews, distance])
    return data

def main():
    driver = setup_driver()
    base_url = 'https://you.ctrip.com/sight/chengdu104/s0-p{}.html'
    all_data = []
    for page in range(1, 301):
        url = base_url.format(page)
        driver.get(url)
        time.sleep(3)  # 等待页面加载
        data = parse_page(driver)
        all_data.extend(data)
        print(f'Page {page} processed.')
    driver.quit()
    df = pd.DataFrame(all_data, columns=['Name', 'Heat', 'Score', 'Price', 'Location', 'Reviews', 'Distance'])
    df.to_excel('Chengdu_Sights.xlsx', index=False)

if __name__ == '__main__':
    main()
