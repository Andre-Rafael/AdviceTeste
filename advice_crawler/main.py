from logging import info
from pathlib import Path
from typing import Any

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from repository.save_data_sqlite import SaveDataSqlite
from repository.save_data_json import SaveDataJson
from mixin.save_data_mixin import SaveDataMixin

from page.tjmg_page_object import TjmgPageObject
from dotenv import load_dotenv

class AdviceCrawler:

    def create_webdriver(self):
        info("Criando webdriver...")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def run(self, nome_cliente: str, url: str):
        save_data_sqlite = SaveDataSqlite()
        with self.create_webdriver() as webdriver:
            tjmg_page = TjmgPageObject(webdriver)
            tjmg_page.navigate(url)
            tjmg_page.search_client(nome_cliente)
            for process_data in tjmg_page.get_result(nome_cliente):
                self.save_data([process_data], SaveDataJson())
                self.save_data(process_data, save_data_sqlite)

    def save_data(self, all_process: list[Any], save_data_mode: SaveDataMixin):
        try:
            save_data_mode.save(all_process)
            info("Dados inseridos com sucesso")
        except Exception:
            info("Erro ao salvar dados")

if __name__ == "__main__":
    load_dotenv('.env')
    url = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
    advice_crawler = AdviceCrawler()
    names_to_search = [
        "ADILSON DA SILVA",
        "JOÂO DA SILVA MORAES",
        "RICARDO DE JESUS",
        "SERGIO FIRMINO DA SILVA",
        "HELENA FARIAS DE LIMA",
        "PAULO SALIM MALUF",
        "PEDRO DE SÁ"
    ]

    [advice_crawler.run(name, url) for name in names_to_search]