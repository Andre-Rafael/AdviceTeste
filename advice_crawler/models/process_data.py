from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Subject:
    codigo: str
    descricao: str
    principal: bool


@dataclass
class CapaProcesso:
    process_number: str
    data_autuacao: datetime
    situacao: str
    orgao_julgador: str
    juiz: str
    classe_acao: str


@dataclass
class PartesRepresentantes:
    titulo: str
    pessoa: str


@dataclass
class InformacoesAdicionais:
    valor_causa: Decimal
    antecipacao_tutela: bool
    autor_manifesta_desinteresse_conciliacao: bool
    crianca_adolescente: bool
    justica_gratuita: bool
    opção_por_juizo_100perc_digital: bool
    pessoa_com_deficiência: bool
    peticao_urgente: bool
    processo_digitalizado: bool
    reconvencao: bool
    renuncia_excede_60_sal: Optional[bool]
    vista_ministerio_publico: bool


@dataclass
class Atualizacao:
    ordem_evento: str
    data_hora: datetime
    descricao: str
    usuario: str
    documentos: Optional[str]
    

@dataclass
class ProcessData:
    name: str
    capa_processo: CapaProcesso
    subjects: list[Subject]
    partes_e_representantes: list[PartesRepresentantes]
    info_adicionais: InformacoesAdicionais
    atualizacoes: list[Atualizacao]