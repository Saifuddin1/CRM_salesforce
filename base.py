import random
import traceback
from time import sleep
from typing import Any, Optional, Union

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

DEBUG = False
StrOrInt = Union[str, int]


class BaseBot:
    base_url: str = 'https://www.google.com'
    min_sleep_time_in_sec: int
    max_sleep_time_in_sec: int
    run_headless: bool = True
    main_driver: bool = True

    extensions_dir: str = 'extensions'

    def __init__(self, min_sleep_time_in_sec: StrOrInt = 1,
                 max_sleep_time_in_sec: StrOrInt = 10) -> None:
        self.min_sleep_time_in_sec = int(min_sleep_time_in_sec)
        self.max_sleep_time_in_sec = int(max_sleep_time_in_sec)

        if self.main_driver:
            self.driver = self.get_browser()
        else:
            self.driver = None

    def get_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=chrome_options)
        return driver

    def trace_error(self, msg: Optional[str] = None) -> None:
        if DEBUG:
            print(msg)
            print(traceback.format_exc())

    def print_bar(self):
        print('------------------------------------------------------------------')

    def sleep_until_presense_of_element(self, element_css_selector: str):
        try:
            element_present = EC.presence_of_element_located(
                (By.CSS_SELECTOR, element_css_selector))
            WebDriverWait(self.driver, 10).until(element_present)
        except Exception:
            self.trace_error()

    def sleep_until_create_post_button_visible(self, element_css_selector: str):
        try:
            element_present = EC.presence_of_element_located(
                (By.CSS_SELECTOR, element_css_selector))
            WebDriverWait(self.driver, 100).until(element_present)
        except Exception:
            self.trace_error()

    def open_base_page(self) -> None:
        print("opening base page!!!!!!!!!")
        assert self.driver is not None
        self.driver.maximize_window()
        self.driver.get(self.base_url)

    def close_bot(self) -> None:
        assert self.driver is not None
        self.driver.close()
        del self.driver

    def random_bot_sleep(self) -> None:
        sleep(random.uniform(0.1, 0.35))

    def random_user_sleep(self) -> None:
        sleep(random.randint(self.min_sleep_time_in_sec, self.max_sleep_time_in_sec))

    def type_text_slowly(self, element: Any, text_to_type: str) -> None:
        for char in text_to_type:
            element.send_keys(char)
            self.random_bot_sleep()

    def change_focus_from_input(self, element: Any) -> None:
        element.send_keys(Keys.TAB)
        self.random_bot_sleep()

    def select_all_text_in_input(self, element: Any) -> None:
        element.send_keys(Keys.CONTROL, 'a')
        self.random_bot_sleep()
