import time
from typing import Any
from selenium.webdriver.common.by import By  # type: ignore
import pandas as pd
from base import BaseBot


class ConsultingScrapeperBot(BaseBot):
    base_url: str = "https://appexchange.salesforce.com/consulting"
    file_name = 'output.xlsx'
    clicked = 0
    run_headless: bool = True
    driver: Any

    def __init__(self, ) -> None:
        super().__init__()

    def get_communication_channel(self) -> dict:
        communication_channel = {"heaqd_quarter": "Na",
                                 "website": "Na", "email": "Na", "phone": "Na"}
        website_css = "a[data-event = 'listing-publisher-website']"
        self.sleep_until_presense_of_element(website_css)
        try:
            website = self.driver.find_element(
                By.CSS_SELECTOR, website_css)
            communication_channel['website'] = website.text
        except Exception as ex:
            ...
        email_css = "a[data-event = 'listing-publisher-email']"
        self.sleep_until_presense_of_element(email_css)
        try:
            email = self.driver.find_element(
                By.CSS_SELECTOR, email_css)
            communication_channel['email'] = email.text
        except Exception as ex:
            ...
        phone_css = "#AppxConsultingListingDetail\:AppxLayout\:listingDetailOverviewTab\:appxListingDetailOverviewTabComp\:j_id768 > div.appx-extended-detail-subsection-description"
        self.sleep_until_presense_of_element(phone_css)
        try:
            phone = self.driver.find_element(
                By.CSS_SELECTOR, phone_css)
            communication_channel['phone'] = phone.text
        except Exception as ex:
            ...
        office_location_css = "#AppxConsultingListingDetail\:AppxLayout\:listingDetailOverviewTab\:appxListingDetailOverviewTabComp\:j_id760 > div.appx-extended-detail-subsection-description.slds-truncate"
        self.sleep_until_presense_of_element(office_location_css)
        try:
            location = self.driver.find_element(
                By.CSS_SELECTOR, office_location_css)
            communication_channel['heaqd_quarter'] = location.text
        except Exception as ex:
            ...
        return communication_channel

    def get_company_name(self) -> str:
        company_name = "Na"
        company_name_css = "#consulting-header-bar-title-id"
        self.sleep_until_presense_of_element(company_name_css)
        try:
            company_name = self.driver.find_element(
                By.CSS_SELECTOR, company_name_css)
            company_name = company_name.text
        except Exception as ex:
            ...
        return company_name.upper()

    def get_cities(self) -> list:
        cities_list = []

        try:
            all_cities_css = "div[class*='appx-detail-subsection-values'] div span[class='appx-detail-subsection-values']"
            self.sleep_until_create_post_button_visible(all_cities_css)
            all_cities = self.driver.find_elements(
                By.CSS_SELECTOR, all_cities_css)
            for city in all_cities:
                cities_list.append(city.text)
        except Exception as ex:
            ...

        # try:
        #     all_cities_link_css = "div[class*='appx-detail-subsection-values'] div a span"
        #     self.sleep_until_presense_of_element(all_cities_link_css)
        #     all_cities_link = self.driver.find_elements(
        #         By.CSS_SELECTOR, all_cities_link_css)
        #     print("print in try block.............")
        #     print("len of", len(all_cities_link))
        #     for all_cities in all_cities_link:
        #         cities_list.append(all_cities.text)
        # except Exception as ex:
        #     print("exception is :", ex)
        #     print("print in except block...............")
        #     ...
        return cities_list

    def get_reputation_score(self):
        # it is on Reviews tab
        reputation_score = "Na"
        reputation_score_css = "div[class='appx-average-rating-numeral']"
        self.sleep_until_presense_of_element(reputation_score_css)
        print("my name is sifuddin...................")
        try:
            reputation_score = self.driver.find_element(
                By.CSS_SELECTOR, reputation_score_css)
            reputation_score = reputation_score.text
        except Exception as ex:
            reputation_score = "Some Error"
        return reputation_score

    def get_market_capitalization(self) -> str:
        a = ""
        return "Na"

    def get_size_of_work(self) -> str:
        return "Na"

    def get_expertise(self) -> list:
        expertise_list = []
        try:
            all_expertise_css = "ul[id='appx_accordion_products'] li[class*='slds-a']"
            self.sleep_until_presense_of_element(all_expertise_css)
            all_expertise = self.driver.find_elements(
                By.CSS_SELECTOR, all_expertise_css)
            for expertise in all_expertise:
                expertise_list.append(expertise.get_attribute('psa-title'))
        except Exception as ex:
            ...
        return expertise_list

    def get_awards_won(self):
        awards_won_list = []
        try:
            awards_won_css = "ul[id='appx_accordion_certifications'] li[class*='slds-a'] span[class='appx-accordion-btn__text-title']"
            self.sleep_until_presense_of_element(awards_won_css)
            awards_won = self.driver.find_elements(
                By.CSS_SELECTOR, awards_won_css)
            for award in awards_won:
                awards_won_list.append(award.text)
        except Exception as ex:
            ...
        return awards_won_list

    def save_data_into_excel(self, data):
        try:
            dataframe1 = pd.read_excel(self.file_name)
            dataframe1.loc[len(dataframe1.index)] = [
                data['COMPANY_NAME'],
                data['OFFICE_LOCATION'],
                data['WEBSITE'],
                data['EMAIL'],
                data['PHONE'],
                data['CITIES_THEY_OFFER_SERVICES'],
                data['MARKET_CAPITALIZATION'],
                data['SIZE_OF_WORK'],
                data['EXPERTISE'],
                data['AWARDS_WON'],
                data['REPUTATION_SCRORE'],
            ]
            dataframe1.to_excel(self.file_name, index=False)
        except IOError:
            df = pd.DataFrame(data=data, index=[1])
            df.to_excel(self.file_name, index=False)

    def load_page_correctly(self):
        while True:
            try:
                self.clicked += 1
                show_more_button_css = "button[id = 'appx-load-more-button-id']"
                self.sleep_until_presense_of_element(show_more_button_css)
                show_more_button = self.driver.find_element(
                    By.CSS_SELECTOR, show_more_button_css)
                show_more_button.click()
            except Exception as ex:
                break

    def start_process(self) -> None:
        self.load_page_correctly()
        all_companies_div_css = "ul[class='appx-tiles-grid-ul'] li a"
        self.sleep_until_presense_of_element(all_companies_div_css)
        all_companies_div = self.driver.find_elements(
            By.CSS_SELECTOR, all_companies_div_css)

        for company_div in all_companies_div:
            self.driver.execute_script("arguments[0].click();", company_div)
            # extract all data on overview tab
            company_name = self.get_company_name()
            communication_channel = self.get_communication_channel()
            office_location = communication_channel['heaqd_quarter']
            webiste = communication_channel['website']
            email = communication_channel['email']
            phone = communication_channel['phone']
            cities_they_offer_services = self.get_cities()

        # we still need to figure it out
        # market_capitalization = self.get_market_capitalization()
        # size_of_work = self.get_size_of_work()  # we still need to figure it out

        # # extract all data on experties tab
        # experties_css = "#tab-default-3__item"
        # self.sleep_until_presense_of_element(experties_css)
        # experties = self.driver.find_element(
        #     By.CSS_SELECTOR, experties_css)
        # self.driver.execute_script("arguments[0].click();", experties)
        # print("yes........... after experties.........")
        # time.sleep(3)
        # expertise = self.get_expertise()
        # awards_won = self.get_awards_won()

        # # extract all data on reviews tab
        # reviews_css = "a[id='tab-default-2__item']"
        # self.sleep_until_presense_of_element(reviews_css)
        # reviews = self.driver.find_element(
        #     By.CSS_SELECTOR, reviews_css)

        # self.driver.execute_script("arguments[0].click();", reviews)
        # print("YES......ON......REVIEW.....PAGE")
        # time.sleep(10)
        # reputation_score = self.get_reputation_score()
        # time.sleep(2)

        # data = {
        #     "COMPANY_NAME": company_name,
        #     "OFFICE_LOCATION": office_location,
        #     "WEBSITE": webiste,
        #     "EMAIL": email,
        #     "PHONE": phone,
        #     "CITIES_THEY_OFFER_SERVICES": " , ".join(cities_they_offer_services),
        #     "MARKET_CAPITALIZATION": market_capitalization,
        #     "SIZE_OF_WORK": size_of_work,
        #     "EXPERTISE": " , ".join(expertise),
        #     "AWARDS_WON": " , ".join(awards_won),
        #     "REPUTATION_SCRORE": reputation_score
        # }
        # self.save_data_into_excel(data)
        # break

    def main_function(self) -> None:
        try:
            self.open_base_page()
            self.start_process()
        except Exception as ex:
            print("EXCEPTION IS :", ex)
            return


if __name__ == '__main__':
    consulting_scrapeper_bot = ConsultingScrapeperBot()
    consulting_scrapeper_bot.main_function()
