from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class AssuntoDTO:
    codigo: str
    descricao: str
    principal: bool


@dataclass
class CapaProcessoDTO:
    process_number: str
    data_autuacao: datetime
    situacao: str
    orgao_julgador: str
    juiz: str
    classe_acao: str


@dataclass
class PartesRepresentantesDTO:
    titulo: str
    nome: str


@dataclass
class InformacoesAdicionaisDTO:
    valor_causa: Decimal
    antecipacao_tutela: str
    autor_manifesta_desinteresse_conciliacao: bool
    crianca_adolescente: bool
    justica_gratuita: bool
    opcao_por_juizo_100perc_digital: bool
    pessoa_com_deficiencia: bool
    peticao_urgente: bool
    processo_digitalizado: bool
    reconvencao: bool
    renuncia_excede_60_sal: Optional[bool]
    vista_ministerio_publico: bool


@dataclass
class AtualizacaoDTO:
    ordem_evento: str
    data_hora: datetime
    descricao: str
    usuario: str
    documentos: Optional[str]
    

@dataclass
class ProcessDataDTO:
    name: str
    capa_processo: CapaProcessoDTO
    assuntos: list[AssuntoDTO]
    partes_e_representantes: list[PartesRepresentantesDTO]
    info_adicionais: InformacoesAdicionaisDTO
    atualizacoes: list[AtualizacaoDTO]