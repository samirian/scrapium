from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv


class Chrome_Options:
    def __init__(self):
        self.proxy              = None
        self.download_directory = None
        self.headless           = False
        self.driver_path        = None
        self.wait_timeout       = 20
        self.page_load_timeout  = 0

    def initiate(self):
        """Returns new driver, wait and actions.
        """
        self.driver = self.get_driver(self.driver_path, self.page_load_timeout)
        self.wait   = self.get_wait(self.driver, self.wait_timeout)
        self.actions= self.get_actions(self.driver)

    def terminate(self):
        """Closes currently opened drivers and performs the cleanup.
        """
        self.driver.close()

    def get_options(self) -> webdriver.ChromeOptions:
        chrome_options  = webdriver.ChromeOptions()
        prefs           = {}
        if self.download_directory != None:
            prefs["download.default_directory"] = self.download_directory
        if self.proxy != None:
            chrome_options.add_argument('--proxy-server=%s' % self.proxy)
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

    def get_driver(self, driver_path:str=None, page_load_timeout: int=0) -> webdriver.Chrome:
        options = self.get_options()
        if driver_path != None:
            driver = webdriver.Chrome(options=options, executable_path=driver_path)
        else:
            driver = webdriver.Chrome(options=options)
        if page_load_timeout != 0:
            driver.set_page_load_timeout(page_load_timeout)
        return driver

    def get_wait(self, driver: webdriver.Chrome, wait_timeout: int) -> WebDriverWait:
        return WebDriverWait(driver, wait_timeout)

    def get_actions(self, driver: webdriver.Chrome) -> ActionChains:
        return ActionChains(driver)

    def set_page_load_timeout(self, timeout: int):
        """Sets a page loading and driver wait timeout in seconds.
        """
        self.page_load_timeout = timeout
        try:
            self.driver.set_page_load_timeout(self.page_load_timeout)
            return True
        except:
            return False

    def set_wait_timeout(self, timeout: int):
        """Sets a timeout for the driver wait class in seconds.
        """
        self.wait_timeout = timeout
        try:
            self.wait = self.get_wait(self.driver, self.wait_timeout)
            return True
        except:
            return False

    def set_proxy(self, ip: str, port: str):
        """Sets the proxy.

        The proxy can be set only before initiating a driver.
        """
        self.proxy = ip + ':' + port

    def set_default_download_directory(self, directory: str):
        """Sets the default download directory.

        The default download directory can be set only before initiating a driver.
        """
        self.download_directory = directory

    def set_driver_executable_path(self, path: str):
        """Sets the driver executable path.

        The driver executable path can be set only before initiating a driver.
        """
        self.driver_path = path

    def set_headless(self, headless: bool):
        """Set the headless state.

        The headless state can be set only before initiating a driver.
        """
        self.headless = headless



class Selenium_Scraper(Process):
    def __init__(self, driver_name: str):
        """Creates a process that includes a driver.

        driver_name = 'chrome' -> chromedriver
        """
        Process.__init__(self)
        if driver_name == 'chrome':
            self.options            = Chrome_Options()

    def open_url(self, url: str, trials: int = 1) -> bool:
        """Tries to open the url page for trials times.
        
        Returns True if the page is loaded successfully
        and False othewise.
        """
        for i in range(trials):
            try:
                self.driver.get(url)
                return True
            except TimeoutException:
                pass
        return False

    def wait_for_element_visibility(self, xpath: str):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def click_element_by_xpath(self, xpath: str):
        self.wait_for_element_visibility(xpath)
        self.driver.find_element_by_xpath(xpath).click()

    def click_element_by_xpath_using_actions(self, xpath: str):
        """Move to element`s postion, then click it using actions.
        """
        self.wait_for_element_visibility(xpath)
        element = self.driver.find_element_by_xpath(xpath)
        self.actions.move_to_element(element).click().perform()

    def get_text_from_element_by_xpath(self, xpath: str) -> str:
        """Get text from the element specified py the parent and xpath.
        """
        self.wait_for_element_visibility(xpath)
        return self.driver.find_element_by_xpath(xpath).text

    def clear_element_text(self, xpath: str):
        """Clears the text inside the element.
        """
        self.wait_for_element_visibility(xpath)
        self.driver.find_element_by_xpath(xpath).clear()

    def send_keys_to_element(self, xpath: str, keys: str):
        """Fill in the element with the given keys string.
        """
        self.wait_for_element_visibility(xpath)
        self.driver.find_element_by_xpath(xpath).send_keys(keys)

    def send_keys_using_actions(self, xpath: str, keys: str):
        """Fill in the element given by the xpath with the given keys string.
        """
        self.wait_for_element_visibility(xpath)
        self.actions.send_keys(keys)

    def extractor(self, element) -> list:
        parsed_element = None
        if type(element) == list:
            parsed_element = []
            for item in element:
                parsed_element.append(self.extractor(item))
        elif type(element) == dict:
            parsed_element = {}
            for key, value in element.items():
                parsed_element[key] = self.extractor(value)
        elif type(element) == str:
            parsed_element = self.get_text_from_element_by_xpath(element)
        return parsed_element

    def extract(self, element: dict) -> str:
        """Extracts the text according to the givien dict xpahs.
        
        elements is in the form of {
            'key1' : 'xpath1',
            'key2' : {
                'key3' : 'xpath3',
                'key4' : 'xpath4',
            },
            'key5' : [
                {
                    'key6' : 'xpath6',
                },
            ]
        }
        """
        if type(element) != dict:
            return None
        return extractor(element)

    def get_csv_file_reader(self, filename: str) -> csv.DictReader:
        """Opens csv file and returns the csv reader.
        """
        csv_file = open(filename, newline='')
        return csv.DictReader(csv_file)

    def get_csv_file_writer(self, filename: str, fieldnames: list, previlage: str) -> (csv.DictWriter, open):
        """Opens csv file and writes the header and returns the file writer.
        """
        csv_file = open(filename, previlage, newline='')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        return writer, csv_file

    def set_state_parameters(state_filename: str, state_fieldnames: list):
        pass

    def save_state(self, *args):
        self.fieldnames
        state = {}
        for arg, fieldname in zip(args, self.fieldname):
            state[fieldname] = arg

    def load_state(self):
        pass

    def initiate(self):
        self.options.initiate()
        self.driver = self.options.driver
        self.wait   = self.options.wait
        self.actions= self.options.actions

    def run(self):
        self.initiate()

    def execute(self, *args):
        """This function should be overriden to pass custom arguments to the
        run function and also to set up the options.
        Example : self.arg1 = args[0]
        """
        self.start()
