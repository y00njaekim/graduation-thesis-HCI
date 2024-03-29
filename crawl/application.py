import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from crawl.constants import CHAMPION_LIST
from crawl.sheet import update_csv


def get_video_info(crawler, url):
    crawler.get_url(url)
    WebDriverWait(crawler.driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#contents > ytd-rich-grid-row ytd-rich-item-renderer")
        )
    )

    count = 0
    last_page_height = crawler.get_scroll_height()
    while True:
        crawler.scroll_to_bottom()
        time.sleep(1.0)
        new_page_height = crawler.get_scroll_height()
        if last_page_height == new_page_height:  # 로딩 중
            time.sleep(4.0)
            if last_page_height == crawler.get_scroll_height():  # 로딩 할 게 없다고 추정
                break
        else:  # 로딩 완료
            last_page_height = new_page_height

        videos = crawler.crawl_items(
            By.CSS_SELECTOR, "#contents > ytd-rich-grid-row ytd-rich-item-renderer"
        )
        appended_vidoes = videos[count:]
        count = len(videos)
        result = []
        for video in appended_vidoes:
            title = video.find_element(
                By.CSS_SELECTOR, "yt-formatted-string#video-title"
            ).text
            champions = [word for word in title.split() if word in CHAMPION_LIST]
            champion = champions[0] if champions else "NULL"
            href = video.find_element(
                By.CSS_SELECTOR, "ytd-thumbnail a#thumbnail"
            ).get_attribute("href")
            
            result.append({"title": title, "champion": champion, "href": href})
        update_csv(result, "output_data/video_data.csv")
        print(f"크롤링 완료: {count}개의 영상")

