from selenium_scraper import Selenium_Scraper

class Scraper(Selenium_Scraper):
    def __init__(self, driver_name):
        """This class scraps the first 80 https proxies available on 
        the website : "https://free-proxy-list.net/"
        """
        Selenium_Scraper.__init__(self, driver_name)

    def run(self):
        print('Hi, I am the scraper class and I run in a separate process.')
        super().run()
        self.open_url("https://free-proxy-list.net/", 3)
        self.click_element_by_xpath('/html/body/section[1]/div/div[2]/div/div[1]/div[1]/div/label/select/option[3]')
        self.click_element_by_xpath('//*[@id="proxylisttable"]/tfoot/tr/th[7]/select/option[3]')
        csv_writer, csv_file = self.get_csv_file_writer('proxy_list', ['ip', 'port', 'country'], 'w')

        try:
            for i in range(80):
                row_dictionary              = {}
                row_xpath                   = '//*[@id="proxylisttable"]/tbody/tr[' + str(i + 1) + ']'
                ip_xpath                    = row_xpath + '/td[1]'
                row_dictionary['ip']        = self.get_text_from_element_by_xpath(ip_xpath)
                port_xpath                  = row_xpath + '/td[2]'
                row_dictionary['port']      = self.get_text_from_element_by_xpath(port_xpath)
                country_xpath               = row_xpath + '/td[3]'
                row_dictionary['country']   = self.get_text_from_element_by_xpath(country_xpath)
                csv_writer.writerow(row_dictionary)
        except:
            pass
        csv_file.close()
        self.options.terminate()

    def execute(self, *args):
        """This function should be overriden to pass custom arguments to the
        run function and also to set up the options.
        Example : self.arg1 = args[0]
        """
        self.options.set_proxy('186.225.63.134', '38459')
        self.options.set_page_load_timeout(60)
        self.options.set_wait_timeout(5)
        super().execute(*args)

if __name__ == "__main__":
    """This is just an example to show how to use Selenium_Scraper class.
    """
    scraper = Scraper('chrome')
    scraper.execute()
    print('Hi, I am the main process and continued nonblocking.')
