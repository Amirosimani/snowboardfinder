import time
import re
import base64
import hashlib
import logging
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

logging.basicConfig(format='%(asctime)s %(levelname)s %(process)d --- %(name)s %(funcName)20s() : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class Scraper:
    logger = logging.getLogger('ImageScraper')

    def __init__(self):
        self._tmp_folder = '/tmp/img-scrpr-chrm/'
        self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                                       options=self.__get_default_chrome_options())

    @staticmethod
    def get_tables(html_table):
        table_value = []
        tag = ['th', 'tr', 'td']

        # You can find children with multiple tags by passing a list of strings
        rows = html_table.findChildren(tag)

        for row in rows:
            cells = row.findChildren(tag)
            for cell in cells:
                value = cell.string
                if value:
                    table_value.append(value.strip())
                    # print("The value in this cell is %s" % value)
                else:
                    table_value.append("None")
        return dict(zip(table_value[::2], table_value[1::2]))

    def parse_page(self, url):

        # get the html file
        page = requests.get(url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')

            # get all the tables
            tables = soup.findChildren('table')

            # only the first 4 tables are useful
            tables = tables[:4]

            # UPPER LEFT TABLE
            table_ul = self.get_tables(tables[0])

            # UPPER RIGHT TABLE
            rows_html = tables[1].findAll("span", {"class": lambda x: x and x.startswith("rating")})
            rows = [x.get_text() for x in rows_html]
            table_ur = dict(zip(rows[::2], rows[1::2]))

            #         # BUTTOM TABLES

            #         table_b = {}
            #         for t in tables[2:]:
            #             l = get_tables(t, ['td', 'p', 'tr'])
            #             table_b.update(l)

            all_items = {**table_ul, **table_ur}

        else:
            print(page.status_code)

        return all_items

    @staticmethod
    def get_date(input_text):

        year = re.findall('[0-9]{4}', input_text)

        return year

    @staticmethod
    def hashme(x):
        return base64.b64encode(hashlib.sha1(x).digest())

    def get_all_boards(self, gender):

        browser = self.driver
        browser.get("https://thegoodride.com/snowboard-reviews/?{}=1".format(gender))
        time.sleep(1)

        button = browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/form/div[1]/div[42]/a')
        browser.execute_script("arguments[0].click();", button)
        time.sleep(400)
        html = browser.page_source

        browser.close()

        return html

    def scraper(self):

        today = datetime.today().strftime('%Y%m%d')
        genders = ['mens', 'womens']

        for g in genders:

            raw_html = self.get_all_boards(g)

            soup = BeautifulSoup(raw_html, "html.parser")
            rows_html = soup.findAll("div", {"class": "board-reviews animate"})

            all_boards = []

            for board in rows_html:
                board_name = board.select('h4')[0].text.strip()
                review_url = board.select('a', href=True)[0]['href']
                all_boards.append([board_name, review_url])

            df_url = pd.DataFrame(all_boards, columns=['board_name', 'url'])
            print(df_url.shape)

            # df_url.to_csv('../data/all_{}_boards.csv'.format(g), index=False)

            rating_list = []
            for url in tqdm(df_url['url']):
                d = self.parse_page(url)
                assert len(d) == 18
                rating_list.append(d)
                time.sleep(.1)

            df_rating = pd.DataFrame(rating_list)
            df_final = pd.concat([df_url, df_rating], axis=1)
            df_final['year'] = df_final['url'].apply(self.get_date)
            df_final['gender'] = g

            df_final['id'] = df_final['url'].astype(str).str.encode('UTF-8').apply(self.hashme)
            df_final['id'] = df_final['id'].apply(lambda x: x.decode('utf-8'))

            df_final = df_final.dropna()
            print(df_final.head())

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
