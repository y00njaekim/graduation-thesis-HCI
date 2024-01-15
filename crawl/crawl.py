from selenium import webdriver


class DriverSingleton:
    _instance = None

    def __new__(cls, headless: bool = False):
        if cls._instance is None:
            if headless:
                headlessoptions = webdriver.ChromeOptions()
                headlessoptions.add_argument("headless")
                headlessoptions.add_argument("window-size=1920x1080")
                headlessoptions.add_argument("disable-gpu")
                agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                headlessoptions.add_argument(agent)
                headlessoptions.add_argument("lang=ko_KR")
                driver = webdriver.Chrome(options=headlessoptions)
            else:
                driver = webdriver.Chrome()
            cls._instance = driver
        return cls._instance


class WebCrawler:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = self.get_driver()

    def get_driver(self):
        return DriverSingleton(self.headless)

    def get_url(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            print("URL 연결 실패: ", url)
            print("오류: ", e)
            return []

    def get_scroll_height(self):
        return self.driver.execute_script(
            "return document.documentElement.scrollHeight"
        )

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
        )

    def crawl_item(self, by, query, is_preprocess=False):
        if is_preprocess:
            return self.preprocess(self.driver.find_element(by, query))
        else:
            return self.driver.find_element(by, query)

    def crawl_items(self, by, query, is_preprocess=False):
        if is_preprocess:
            return self.preprocess(self.driver.find_elements(by, query))
        else:
            return self.driver.find_elements(by, query)

    def preprocess(self, elems):
        pass

    def close(self):
        self.driver.quit()


class any_of_elements_present:
    def __init__(self, locators):
        self.locators = locators

    def __call__(self, driver):
        for locator in self.locators:
            if driver.find_elements(*locator):
                return True
        return False
