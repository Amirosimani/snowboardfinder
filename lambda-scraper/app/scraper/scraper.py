import logging
import time
import hashlib
import base64
from tqdm import tqdm
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(format='%(asctime)s %(levelname)s %(process)d --- %(name)s %(funcName)20s() : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class GearScraper:
    logger = logging.getLogger('GearScraper')

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def parse(self, gender):

        board_list = []
        single_board_dict = {}

        url_list = self.__get_boards_url(gender, self.driver)
        for url in tqdm(url_list[:2], desc="Getting ratings..."):
            single_board_dict['id'] = self.__hashme(url)
            single_board_dict['ratings'] = self.__get_ratings(url, self.driver)
            single_board_dict['meta_data'] = self.__get_meta_data(url, self.driver)
            board_list.append(single_board_dict)
        self.logger.info("All boards have been processed.")
        #         driver.close()

        return board_list

    @staticmethod
    def __hashme(x):
        return base64.b64encode(hashlib.sha1(x.encode('UTF-8')).digest())

    def __get_boards_url(self, gender, browser):
        search_url = f"https://thegoodride.com/snowboard-reviews/?{gender}=1"
        board_urls = []

        browser.get(search_url)
        # click and wait
        button = browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/form/div[1]/div[42]/a')
        browser.execute_script("arguments[0].click();", button)
        self.logger.info(f"Loading main page for \033[1m{gender}\033[0m boards...")
        time.sleep(10)

        elems = browser.find_elements_by_xpath('//*[@id="applications"]/*/a[@href]')
        for elem in tqdm(elems, desc="Fetching links "):
            board_urls.append(elem.get_attribute("href"))

        return board_urls

    @staticmethod
    def __get_ratings(url, driver):
        rating_dict = {}
        driver.get(url)

        # top-right table
        elems = driver.find_elements_by_xpath('//*[@id="post-"]/div[1]/div[2]/div[1]/table/tbody/*')
        for row in elems:
            k = row.find_elements_by_tag_name("td")[0]
            v = row.find_elements_by_tag_name("td")[1]
            rating_dict[k.text] = v.text

        # top-left table
        elems = driver.find_elements_by_xpath('//*[@id="post-"]/div[1]/div[2]/div[2]/table/tbody/*')
        for item in [e.text.split() for e in elems]:
            rating_dict[item[0]] = item[1]

        # bottom table
        elems = driver.find_elements_by_xpath('//*[@id="post-"]/div[1]/div[2]/div[3]/*/table/tbody/*')
        for item in [e.text.split() for e in elems]:
            rating_dict[item[0]] = item[1]
        return rating_dict

    @staticmethod
    def __get_meta_data(url, driver):

        meta_dict = {}

        driver.get(url)
        meta_dict['name'] = url.rsplit('/', 1)[1]
        meta_dict['url'] = url

        # Get price data
        for e in driver.find_elements_by_xpath('//*[@id="post-"]/div[1]/div[1]/div/div[1]'):
            meta_dict['price'] = e.text.rsplit(' ', 1)[1]

        # get image url
        for e in driver.find_elements_by_xpath('//*[@id="post-"]/div[1]/div[1]/div/div[2]/a'):
            meta_dict['image_url'] = e.get_attribute("href")

        return meta_dict

    def close_connection(self):
        self.driver.quit()
