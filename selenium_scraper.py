from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import csv


class Selenium_Scraper(Process):
    def __init__(self):
        """Creates a process that includes a chromedriver.
        """
        Process.__init__(self)
        self.proxy              = None
        self.download_directory = None
        self.timeout            = None

    def get_csv_file_reader(self, filename: str) -> csv.DictReader:
        '''
        Opens csv file and returns the csv reader.
        '''
        csv_file = open(filename, newline='')
        return csv.DictReader(csv_file)

    def get_csv_file_writer(self, filename: str, fieldnames: list, previlage: str) -> (csv.DictWriter, open):
        '''
        Opens csv file and writes the header and returns the file writer.
        '''
        csv_file = open(filename, previlage, newline='')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        return writer, csv_file

    def set_default_download_directory(self, directory: str):
        """Sets the default download directory.
        """
        self.download_directory = directory

    def set_proxy(self, ip: str, port: str):
        """Sets the proxy.
        """
        self.proxy = ip + ':' + port

    def set_timeout(self, timeout: int):
        """Sets a page loading and driver wait timeout in seconds.
        """
        self.timeout = timeout

    def __get_options(self) -> webdriver.ChromeOptions:
        chrome_options = webdriver.ChromeOptions()
        prefs = {}
        if self.download_directory != None:
            prefs["download.default_directory"] = self.download_directory
        if self.proxy != None:
            chrome_options.add_argument('--proxy-server=%s' % self.proxy)
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

    def __get_driver_wait_actions(self) -> (webdriver.Chrome, WebDriverWait, ActionChains):
        options = self.__get_options()
        driver  = webdriver.Chrome(options=options)
        wait    = None
        actions = ActionChains(driver)
        if self.timeout != None:
            wait = WebDriverWait(driver, self.timeout)
            driver.set_page_load_timeout(self.timeout)
        return (driver, wait, actions)

    def open_url(self, url):
        self.driver.get(url)

    def get_text_from_element_by_xpath(self, xpath: str) -> str:
        """Get text from the element specified py the parent and xpath.
        """
        self.wait_for_element_visibility(xpath)
        return self.driver.find_element_by_xpath(xpath).text

    def click_element_by_xpath(self, xpath: str):
        self.wait_for_element_visibility(xpath)
        self.driver.find_element_by_xpath(xpath).click()

    def click_element_by_xpath_using_actions(self, xpath: str):
        """Move to element`s postion, then click it using actions.
        """
        self.wait_for_element_visibility(xpath)
        element = self.driver.find_element_by_xpath(xpath)
        self.actions.move_to_element(element).click().perform()

    def wait_for_element_visibility(self, xpath: str):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def send_keys_to_element(self, xpath: str, keys: str):
        """Fill in the element with the given keys string.
        """
        self.driver.find_element_by_xpath(xpath).send_keys(keys)

    def send_keys_using_actions(self, xpath: str, keys: str):
        """Fill in the vurrently selected element with the given keys string.
        """
        self.actions.send_keys(keys)

    def run(self):
        driver, wait, actions = self.__get_driver_wait_actions()
        self.driver = driver
        self.wait   = wait
        self.actions= actions

    def execute(self, *args):
        """This function should be overriden to pass custom argmunts to the
        run function.
        Example : self.arg1 = args[0]
        """
        self.start()
