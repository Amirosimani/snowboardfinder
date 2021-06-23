import time
import json
import base64
import hashlib
import logging
import platform
from tqdm import tqdm
from selenium import webdriver

logging.basicConfig(format='%(asctime)s %(levelname)s %(process)d --- %(name)s %(funcName)20s() : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class GearScraper:
    logger = logging.getLogger('GearScraper')

    def __init__(self):
        current_platform = platform.platform()
        if 'macOS' in current_platform:  # for local run
            logging.info("Local-mode detected...downloading webdriver")
            from webdriver_manager.chrome import ChromeDriverManager
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
        else:   # for running in Lambda
            self._tmp_folder = '/tmp/img-scrpr-chrm/'
            self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                                           options=self.__get_default_chrome_options())

    def parse(self, gender):

        board_list = []
        url_list = self.__get_boards_url(gender, self.driver)

        for url in tqdm(url_list, desc="Getting ratings..."):
            single_board_dict = {}
            single_board_dict['id'] = self.__hashme(url)
            single_board_dict['ratings'] = self.__get_ratings(url, self.driver)
            single_board_dict['meta_data'] = self.__get_meta_data(url, gender, self.driver)
            board_list.append(single_board_dict)
        self.logger.info("All boards have been processed.")

        board_list_json = json.dumps(board_list)
        return board_list_json

    @staticmethod
    def __hashme(x):
        unique_id = base64.b64encode(hashlib.sha1(x.encode('UTF-8')).digest())
        return unique_id.decode('utf-8')

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
    def __get_meta_data(url, gender, driver):

        meta_dict = {}

        driver.get(url)
        meta_dict['name'] = url.rsplit('/', 1)[1]
        meta_dict['gender'] = gender
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

    def __get_default_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()

        lambda_options = [
            '--autoplay-policy=user-gesture-required',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-component-update',
            '--disable-default-apps',
            '--disable-dev-shm-usage',
            '--disable-domain-reliability',
            '--disable-extensions',
            '--disable-features=AudioServiceOutOfProcess',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-notifications',
            '--disable-offer-store-unmasked-wallet-cards',
            '--disable-popup-blocking',
            '--disable-print-preview',
            '--disable-prompt-on-repost',
            '--disable-renderer-backgrounding',
            '--disable-setuid-sandbox',
            '--disable-speech-api',
            '--disable-sync',
            '--disk-cache-size=33554432',
            '--hide-scrollbars',
            '--ignore-gpu-blacklist',
            '--ignore-certificate-errors',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-default-browser-check',
            '--no-first-run',
            '--no-pings',
            '--no-sandbox',
            '--no-zygote',
            '--password-store=basic',
            '--use-gl=swiftshader',
            '--use-mock-keychain',
            '--single-process',
            '--headless']

        # chrome_options.add_argument('--disable-gpu')
        for argument in lambda_options:
            chrome_options.add_argument(argument)
        chrome_options.add_argument('--user-data-dir={}'.format(self._tmp_folder + '/user-data'))
        chrome_options.add_argument('--data-path={}'.format(self._tmp_folder + '/data-path'))
        chrome_options.add_argument('--homedir={}'.format(self._tmp_folder))
        chrome_options.add_argument('--disk-cache-dir={}'.format(self._tmp_folder + '/cache-dir'))

        return chrome_options
