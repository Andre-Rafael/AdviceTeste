from datetime import datetime
from decimal import Decimal
from re import search
from typing import Optional

from bs4 import BeautifulSoup as bs
from dto.process_data import (AssuntoDTO, AtualizacaoDTO, CapaProcessoDTO,
                              InformacoesAdicionaisDTO,
                              PartesRepresentantesDTO, ProcessDataDTO)
from unidecode import unidecode


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

    def extract_data(self, page_source: str, nome_buscado: str) -> ProcessDataDTO:
        soup = bs(page_source, 'html.parser')
        capa_processo: CapaProcessoDTO = self.get_capa_do_processo(soup)

        assunto: list[AssuntoDTO] = self.get_assunto(soup)

        partes_do_processo: list[PartesRepresentantesDTO] \
            = self.read_table_partes(soup)
        

        additional_info: InformacoesAdicionaisDTO = \
            self.get_info_adicionais(soup)

        atualizacoes = self.read_updates_table(soup)
        return ProcessDataDTO(
            nome_buscado,
            capa_processo,
            assunto,
            partes_do_processo,
            additional_info,
            atualizacoes
        )

    def read_updates_table(self, soup: bs) -> list[AtualizacaoDTO]:
        atualizacoes: list[AtualizacaoDTO] = []
        update_table = soup.find_all('table', {"summary":"Assuntos"})[-1]
        for line in update_table.tbody.find_all('tr')[1:]:
            evento, data, descricao, usuario, doc = line.find_all('td')
            atualizacoes.append(AtualizacaoDTO(
                evento.get_text(),
                datetime.strptime(data.get_text(), "%d/%m/%Y %H:%M:%S"),
                descricao.get_text(),
                usuario.get_text(),
                False if "não gerou" in doc.get_text() else True
            ))
        return atualizacoes

    def get_info_adicionais(self, soup: bs) -> InformacoesAdicionaisDTO:
        info_adicionais_element = soup.find(id="fldInformacoesAdicionais").find_all('div')[0].get_text().lower()
        additional_info = InformacoesAdicionaisDTO(
            Decimal(
                self.extract_text_from_regex(
                    r'valor da causa: ([\d\.]+\,\d{2})',
                    info_adicionais_element
                ).replace('.', '').replace(',', '.')
            ),
            self.extract_text_from_regex(r'de tutela: (\D+?)(autor|criança)', info_adicionais_element),
            self.convert_to_bool(self.extract_text_from_regex(r'manifesta desinteresse na conciliação: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'criança e adolescente: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'justiça gratuita: ([A-Za-z]+)', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'opção por juízo 100% digital: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'pessoa com deficiência: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'petição urgente: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'processo digitalizado: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'reconvenção: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'renúncia excedente 60 salários: (\D{3})', info_adicionais_element)),
            self.convert_to_bool(self.extract_text_from_regex(r'ministério público: (\D{3})', info_adicionais_element)),
        )
        return additional_info

    def read_table_partes(self, soup: bs) -> list[PartesRepresentantesDTO]:
        partes_do_processo: list[PartesRepresentantesDTO] = []
        partes_representantes = soup.find(id="fldPartes").tbody.find_all('tr')
        for line in partes_representantes:
            line_is_header = line.find('th')
            if line_is_header:
                header = line.find_all('th')
            else:
                content = line.find_all('td')
                partes_do_processo.extend([
                    PartesRepresentantesDTO(h.text, unidecode(c.text.lower())) for h, c in zip(header, content) if c.text
                ])
        return partes_do_processo

    def get_assunto(self, soup: bs) -> list[AssuntoDTO]:
        subjects: list[AssuntoDTO] = []
        subject_lines = soup.find_all(id="fldAssuntos")[1].find('table').tbody.find_all('tr')[1:]
        for line in subject_lines:
            cod, descr, principal = line.find_all('td')
            subjects.append(AssuntoDTO(
                codigo=cod.text,
                descricao=descr.text.lower(),
                principal=principal.text.lower() == "sim",
            ))
        return subjects

    def get_capa_do_processo(self, soup: bs) -> CapaProcessoDTO:
        capa_processo = soup.find(id='fldAssuntos')
        capa_processo = CapaProcessoDTO(
            capa_processo.find(id="txtNumProcesso").get_text(),
            datetime.strptime(capa_processo.find(id="txtAutuacao").get_text(), "%d/%m/%Y %H:%M:%S"),
            capa_processo.find(id="txtSituacao").get_text().lower(),
            capa_processo.find(id="txtOrgaoJulgador").get_text().lower(),
            capa_processo.find(id="txtMagistrado").get_text().lower(),
            capa_processo.find(id="txtClasse").get_text().lower(),
        )
        return capa_processo