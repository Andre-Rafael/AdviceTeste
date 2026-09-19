from logging import info
from os import getenv
from time import sleep
from typing import Generator

from dto.process_data import ProcessDataDTO
from extractor.tjmg_data_extractor import TjmgDataExtractor
from mixin.tribunal_page_mixin import TribunalPageMixin
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from twocaptcha import TwoCaptcha


class TjmgPageObject(TribunalPageMixin):
    def __init__(self, webdriver: WebDriver):
        super().__init__(webdriver)
        self.tjmg_data_extractor = TjmgDataExtractor()
        self.two_captcha = TwoCaptcha(apiKey=getenv("TOKEN_2CAPTCHA"))


    def navigate(self, url):
        info("Acessando URL")
        return super().navigate(url)

    def search_client(self, client_name: str):
        parts_name_field = self._webdriver.find_element(
            By.ID, 'txtStrParte'
        )
        parts_name_field.send_keys(client_name)
        self._webdriver.find_elements(By.TAG_NAME, 'img')
        img_recaptcha_element: WebElement = self._webdriver.find_element(
            By.XPATH, '//img[@title="Informe o código de confirmação"]'
        )
        result = self.two_captcha.normal(
            img_recaptcha_element.get_attribute('src')
        )
        self._webdriver.find_element(By.ID, "txtInfraCaptcha").send_keys(result['code'].upper())
        self._webdriver.find_element(By.ID, 'sbmNovo').click()
        info(f"Searching for {client_name}")

    def get_result(self, client_name: str) -> Generator[ProcessDataDTO, None, None]:
        sleep(2)
        result_table = WebDriverWait(self._webdriver, 20).until(
            EC.presence_of_element_located((By.ID, 'divInfraAreaTabela'))
        ).find_element(By.TAG_NAME, 'table')
        content_table: list[WebElement] = result_table.find_elements(By.TAG_NAME, 'tr')[1:]
        links = [line.find_element(By.TAG_NAME, 'td').find_element(By.TAG_NAME, 'a').get_attribute('href') for line in content_table if client_name == line.find_elements(By.TAG_NAME, 'td')[0].text]
        info(f"{len(links)} resultados encontrado")
        for link in links:
            self.navigate(link)
            lines = self._webdriver.find_element(By.ID, 'divInfraAreaTabela').find_elements(By.TAG_NAME, 'tr')[1:]
            for i in range(1, len(lines) + 1):
                client_process = self._webdriver.find_element(By.ID, 'divInfraAreaTabela').find_elements(By.TAG_NAME, 'tr')[i]
                num_process = client_process.find_element(By.TAG_NAME, 'a')
                print(num_process.text)
                num_process.click()
                if listar_mais := self._webdriver.find_elements(
                    By.XPATH, '//a[text()="Clique aqui para listar todos os eventos"]'
                ):
                    listar_mais[0].click()
                    sleep(1)
                    yield self.tjmg_data_extractor.extract_data(self._webdriver.page_source, client_name)
                    self._webdriver.back()
                else:
                    yield self.tjmg_data_extractor.extract_data(self._webdriver.page_source, client_name)
                    
                self._webdriver.back()
        self._webdriver.back()


