from logging import info

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from mixin.save_data_mixin import SaveDataMixin

from page.tjmg_page_object import TjmgPageObject
from exception import InvalidException

class AdviceCrawler:

    def create_webdriver(self):
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def run(self, nome_cliente: str):
        url = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
        with self.create_webdriver() as webdriver:
            tjmg_page = TjmgPageObject(webdriver)
            tjmg_page.navigate(url)
            tjmg_page.search_client(nome_cliente)
        all_process = [
            process_data for process_data in tjmg_page.get_result(nome_cliente)
        ]    
        self.save_data(all_process, 'json')

    def save_data(self, all_process: list[DataclassInterface], save_data: SaveDataMixin): # type: ignore
        save_data.save_data(all_process)
        info("Dados inseridos com sucesso")

advice_crawler = AdviceCrawler()
advice_crawler.run("ADILSON DA SILVA")