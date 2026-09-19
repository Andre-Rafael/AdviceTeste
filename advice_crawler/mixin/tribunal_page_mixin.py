from abc import ABC

from selenium.webdriver.remote.webdriver import WebDriver

class TribunalPageMixin(ABC):
    def __init__(self, webdriver: WebDriver):
        self._webdriver: WebDriver = webdriver

    def navigate(self, url: str):
        self._webdriver.get(url)

    def search_client(self, client_name) -> None:
        ...

    def get_result(self):
        ...