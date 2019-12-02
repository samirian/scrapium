from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class Chrome_Options:
    def __init__(self):
        self.proxy              = None
        self.download_directory = None
        self.download_prompt    = None
        self.headless           = False
        self.driver_path        = None
        self.wait_timeout       = 20
        self.page_load_timeout  = 0
        self.sandbox            = True

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
        if self.download_prompt != None:
            prefs["download.prompt_for_download"] = self.download_prompt
        if self.proxy != None:
            chrome_options.add_argument('--proxy-server=%s' % self.proxy)
        if self.headless:
            chrome_options.add_argument('--headless')
        if not self.sandbox:
            chrome_options.add_argument('--no-sandbox')
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

    def set_download_prompt(self, download_prompt: bool):
        """Sets the download prompt
        """
        self.download_prompt = download_prompt

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

    def set_sandbox(self, sandbox: bool):
        """Set the sandbox state.

        The sandbox state can be set only before initiating a driver.
        """
        self.sandbox = sandbox
