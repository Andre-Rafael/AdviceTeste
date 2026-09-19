from datetime import datetime
from decimal import Decimal
from re import search
from typing import Optional

from bs4 import BeautifulSoup as bs

from models.process_data import (
    PartesRepresentantes, CapaProcesso, Subject,
    Atualizacao, InformacoesAdicionais, ProcessData
)

class TjmgDataExtractor:
    def __init__(self):
        pass

    def extract_text_from_regex(self, pattern: str, source_text: str) -> Optional[str]:
        result = search(pattern, source_text)
        return result.group(1).lower() if result else None

    def convert_to_bool(self, text: str) -> Optional[bool]:
        if text is None:
            return None
        else:
            return text == "sim"

    def extract_data(self, page_source: str, nome_buscado: str) -> ProcessData:
        soup = bs(page_source, 'html.parser')
        capa_processo = soup.find(id='fldAssuntos')
        capa_processo = CapaProcesso(
            capa_processo.find(id="txtNumProcesso").get_text(),
            datetime.strptime(capa_processo.find(id="txtAutuacao").get_text(), "%d/%m/%Y %H:%M:%S"),
            capa_processo.find(id="txtSituacao").get_text().lower(),
            capa_processo.find(id="txtOrgaoJulgador").get_text().lower(),
            capa_processo.find(id="txtMagistrado").get_text().lower(),
            capa_processo.find(id="txtClasse").get_text().lower(),
        )

        subjects: list[Subject] = []
        subject_lines = soup.find_all(id="fldAssuntos")[1].find('table').tbody.find_all('tr')[1:]
        for line in subject_lines:
            cod, descr, principal = line.find_all('td')
            subjects.append(Subject(
                codigo=cod.text,
                descricao=descr.text.lower(),
                principal=principal.text.lower() == "sim",
            ))

        partes_do_processo: list[PartesRepresentantes] = []
        partes_representantes = soup.find(id="fldPartes").tbody.find_all('tr')
        for line in partes_representantes:
            line_is_header = line.find('th')
            if line_is_header:
                header = line.find_all('th')
            else:
                content = line.find_all('td')
                partes_do_processo.extend([
                    PartesRepresentantes(h.text, c.text.lower()) for h, c in zip(header, content) if c.text
                ])
        

        info_adicionais_element = soup.find(id="fldInformacoesAdicionais").find_all('div')[0].get_text().lower()
        additional_info = InformacoesAdicionais(
            Decimal(
                self.extract_text_from_regex(
                    r'valor da causa: ([\d\.]+\,\d{2})',
                    info_adicionais_element
                ).replace('.', '').replace(',', '.')
            ),
            self.extract_text_from_regex(r'de tutela: (\D+?)(autor|criança)', info_adicionais_element),
            self.convert_to_bool(self.extract_text_from_regex(r'manifesta desinteresse na conciliação: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'criança e adolescente: (\D{3})', info_adicionais_element)),
            self.extract_text_from_regex(r'justiça gratuita: ([A-Za-z]+)', info_adicionais_element),
            self.convert_to_bool(self.extract_text_from_regex(r'opção por juízo 100% digital: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'pessoa com deficiência: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'petição urgente: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'processo digitalizado: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'reconvenção: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'renúncia excedente 60 salários: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'ministério público: (\D{3})', info_adicionais_element)),
        )

        atualizacoes: list[Atualizacao] = []
        update_table = soup.find_all('table', {"summary":"Assuntos"})[-1]
        for line in update_table.tbody.find_all('tr')[1:]:
            evento, data, descricao, usuario, doc = line.find_all('td')
            atualizacoes.append(Atualizacao(
                evento.get_text(),
                datetime.strptime(data.get_text(), "%d/%m/%Y %H:%M:%S"),
                descricao.get_text(),
                usuario.get_text(),
                False if "não gerou" in doc.get_text() else True
            ))
        return ProcessData(
            nome_buscado,
            capa_processo,
            subjects,
            partes_do_processo,
            additional_info,
            atualizacoes
        )