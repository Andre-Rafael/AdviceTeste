from logging import info
from uuid import UUID, uuid1

from sqlalchemy import create_engine
from dto.process_data import (
    AtualizacaoDTO, ProcessDataDTO, 
    PartesRepresentantesDTO, CapaProcessoDTO,
    InformacoesAdicionaisDTO, AssuntoDTO
)
from mixin.save_data_mixin import SaveDataMixin
from sqlalchemy.orm import sessionmaker

from model.assunto import Assunto
from model.atualizacoes import Atualizacoes
from model.capa_processo import CapaProcesso
from model.dados_processo import DadosProcesso
from model.informacoes_adicionais import InformacaoAdicional
from model.partes_representantes import PartesRepresentantes

class SaveDataSqlite(SaveDataMixin):
    def __init__(self):
        self.engine = create_engine(
            "sqlite:///tjmg.db", echo=True, connect_args={"autocommit": False}
        )

    def atualizacao_to_model(self, dto: list[AtualizacaoDTO], id_processo: UUID) -> list[Atualizacoes]:
        return [
            Atualizacoes(
                ordem_evento=atualizacao.ordem_evento,
                data_hora=atualizacao.data_hora,
                descricao=atualizacao.descricao,
                usuario=atualizacao.usuario,
                documentos=atualizacao.documentos,
                dados_processo_id=id_processo
            )
            for atualizacao in dto
        ]
    
    def assunto_to_model(self, dto: list[AssuntoDTO], id_processo: UUID) -> list[Assunto]:
        return [
            Assunto(
                codigo=assunto.codigo,
                descricao=assunto.descricao,
                principal=assunto.principal,
                dados_processo_id=id_processo
            )
            for assunto in dto
        ]
    
    def partes_representante_to_model(self, dto: list[PartesRepresentantesDTO], id_processo: UUID) -> list[PartesRepresentantes]:
        return [
            PartesRepresentantes(
                titulo=parte_representante.titulo,
                nome=parte_representante.nome,
                dados_processo_id=id_processo
            )
            for parte_representante in dto
        ]
    
    def capa_processo_to_model(self, dto: CapaProcessoDTO, id_processo: UUID) -> CapaProcesso:
        return CapaProcesso(
            process_number=dto.process_number,
            data_autuacao=dto.data_autuacao,
            situacao=dto.situacao,
            orgao_julgador=dto.orgao_julgador,
            juiz=dto.juiz,
            classe_acao=dto.classe_acao,
            dados_processo_id=id_processo
        )
    
    def info_adicional_to_model(self, dto: InformacoesAdicionaisDTO, id_processo: UUID) -> InformacaoAdicional:
        return InformacaoAdicional(
            valor_causa=dto.valor_causa,
            antecipacao_tutela=dto.antecipacao_tutela,
            autor_manifesta_desinteresse_conciliacao=dto.autor_manifesta_desinteresse_conciliacao,
            crianca_adolescente=dto.crianca_adolescente,
            justica_gratuita=dto.justica_gratuita,
            opcao_por_juizo_100perc_digital=dto.opcao_por_juizo_100perc_digital,
            pessoa_com_deficiencia=dto.pessoa_com_deficiencia,
            peticao_urgente=dto.peticao_urgente,
            processo_digitalizado=dto.processo_digitalizado,
            reconvencao=dto.reconvencao,
            renuncia_excede_60_sal=dto.renuncia_excede_60_sal,
            vista_ministerio_publico=dto.vista_ministerio_publico,
            dados_processo_id=id_processo
        )
    
    def dados_processo_to_model(self, nome_pesquisado: str, id_processo: UUID) -> DadosProcesso:
        return DadosProcesso(
            id=id_processo,
            name=nome_pesquisado
        )

    def save(self, data: ProcessDataDTO):
        id_processo = uuid1()
        atualizacao_model = self.atualizacao_to_model(data.atualizacoes, id_processo)
        assunto_model = self.assunto_to_model(data.assuntos, id_processo)
        partes_model = self.partes_representante_to_model(data.partes_e_representantes, id_processo)
        capa_model = self.capa_processo_to_model(data.capa_processo, id_processo)
        info_add_model = self.info_adicional_to_model(data.info_adicionais, id_processo)
        dados_processo_model = self.dados_processo_to_model(data.name, id_processo)
        chain_model = [atualizacao_model, assunto_model, partes_model]

        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            info("Conectado com sucesso!")
            session.add(dados_processo_model)
            session.add(info_add_model)
            session.add(capa_model)
            for model in chain_model:
                session.add_all(model)
            session.commit()
        info("Dados inseridos com sucesso")