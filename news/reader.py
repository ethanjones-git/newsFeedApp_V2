from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


class Reader:
    def __init__(self):
        #Create a webdriver
        self.driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def choose_reader(self,url):
        try:
            if url[12:15] == 'cnn':
                out = self.cnn(url)
            elif url[12:15] == 'msn':
                out = self.msn(url)
            elif url[12:15] == 'cbs':
                out = self.cbs(url)
            elif url[12:17] == 'thegu':
                out = self.guardian(url)
            elif url[12:22] == '.yahoo.com':
                out = self.yahoo(url)
            else:
                out = 'ERROR 01: Reader not created'

        except Exception as e:
            out = "ERROR 02: Unable to scrape: " +str(e)

        return out

    def cnn(self,url):

        self.driver.get(url)

        try:
            content = self.driver.find_element(By.CLASS_NAME, "article-body-commmercial-selector")
            if content is None:
                content = self.driver.find_element(By.CLASS_NAME, "article__main")
                content  = content.text
            else:
                pass

        except NoSuchElementException:
            content = 'no such element'
        return content

    def guardian(self,url):

        self.driver.driver.get(url)

        try:
            content = self.driver.find_element(By.ID, "maincontent")
            content = content.text

        except NoSuchElementException:
            content = 'no such element'

        return content

    def cbs(self,url):
        self.driver.get(url)

        try:
            content = self.driver.find_element(By.CLASS_NAME, "content__body")
            content = content.text

        except NoSuchElementException:
            content = 'no such element'

        return content

    def msn(self,url):

        self.driver.get(url)

        try:
            content = self.driver.find_element(By.CLASS_NAME, "article-content")
            content = content.text
        except NoSuchElementException:
            content = 'No such element'

        return content

    def yahoo(self,url):

        self.driver.get(url)

        try:
            content = self.driver.find_element(By.CLASS_NAME, 'caas-body')
            content = content.text
        except NoSuchElementException:
            content = 'No such element'

        return content

    def kill(self):
        self.driver.quit()

    def close(self):
        self.driver.close()


