from selenium_scraper import Selenium_Scraper

class Scraper(Selenium_Scraper):
    def __init__(self):
        """This class scraps the first 80 https proxies available on 
        the website : "https://free-proxy-list.net/"
        """
        Selenium_Scraper.__init__(self)

    def run(self):
        super().run()
        self.open_url("https://free-proxy-list.net/")
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
        self.driver.close()


    def execute(self, *args):
        self.set_proxy('170.79.16.19', '8080')
        self.set_timeout(60)
        super().execute(*args)

if __name__ == "__main__":
    """This is just an example to show how to use Selenium_Scraper class.
    """
    scraper = Scraper()
    scraper.execute()
