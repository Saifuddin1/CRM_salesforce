import random
import time
from typing import Any
import multiprocessing
import csv
from selenium.webdriver.common.by import By  # type: ignore

from base import BaseBot


class ConsultingScrapeperBot(BaseBot):
    base_url: str = "https://appexchange.salesforce.com/consulting"
    run_headless: bool = True
    driver: Any

    def __init__(self, ) -> None:
        super().__init__()

    def main_function(self) -> None:
        # self.open_base_page()
        self.driver.get(self.base_url)
        time.sleep(10)
        print("starting main function...............")


if __name__ == '__main__':
    consulting_scrapeper_bot = ConsultingScrapeperBot()
    consulting_scrapeper_bot.main_function()
