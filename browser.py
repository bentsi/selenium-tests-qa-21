import time
import logging
from selenium import webdriver


LOGGER = logging.getLogger(__name__)


class UrlNotChanged(Exception):
    pass


class Browser:
    def __init__(self, base_url):
        LOGGER.info("Initializing browser...")
        self._base_url = base_url
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=webdriver.ChromeOptions())
        self.driver.implicitly_wait(5)

    @property
    def base_url(self):
        return self._base_url

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title

    def wait_till_current_url_changes(self, url, timeout=10):
        for try_number in range(timeout):
            if self.current_url == url:
                return True
            time.sleep(0.5)
        raise UrlNotChanged(url)

    def wait_till_js_loaded(self):
        LOGGER.info("Waiting for JS to be loaded...")
        for try_number in range(10):
            res = self.driver.execute_script("return document.readyState")
            if "complete" in str(res):
                return True
            time.sleep(0.5)
        raise Exception(f"JS didn't reach 'complete' state")

    def goto_url(self, url, wait_till_changes=True):
        LOGGER.info(f"Going to url '{url}'...")
        self.driver.get(url=url)
        if wait_till_changes:
            self.wait_till_current_url_changes(url=url)
        self.wait_till_js_loaded()

    def close_tab(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()