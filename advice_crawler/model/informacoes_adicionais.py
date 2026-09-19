from decimal import Decimal
from uuid import uuid1, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .dados_processo import DadosProcesso
from .base import Base, engine

class InformacaoAdicional(Base):
    __tablename__ = "INFORMACAO_ADICIONAL"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid1, name='ID')
    valor_causa: Mapped[Decimal] = mapped_column(name="VALOR_CAUSA")
    antecipacao_tutela: Mapped[str] = mapped_column(name="ANTECIPACAO_TUTELA", nullable=True)
    autor_manifesta_desinteresse_conciliacao: Mapped[bool] = mapped_column(name="AUTOR_MANIFESTA_DESINTERESSE_CONCILIACAO", nullable=True)
    crianca_adolescente: Mapped[bool] = mapped_column(name="CRIANCA_ADOLESCENTE", nullable=True)
    justica_gratuita: Mapped[bool] = mapped_column(name="JUSTICA_GRATUITA", nullable=True)
    opcao_por_juizo_100perc_digital: Mapped[bool] = mapped_column(name="OPCAO_POR_JUIZO_100_DIGITAL", nullable=True)
    pessoa_com_deficiencia: Mapped[bool] = mapped_column(name="PESSOA_COM_DEFICIENCIA", nullable=True)
    peticao_urgente: Mapped[bool] = mapped_column(name="PERTICAO_URGENTE", nullable=True)
    processo_digitalizado: Mapped[bool] = mapped_column(name="PROCESSO_DIGITALIZADO", nullable=True)
    reconvencao: Mapped[bool] = mapped_column(name="RECONVENCAO", nullable=True)
    renuncia_excede_60_sal: Mapped[bool] = mapped_column(name="RENUNCIA_EXCEDE_60_SALARIOS", nullable=True)
    vista_ministerio_publico: Mapped[bool] = mapped_column(name="VISTA_MINISTERIO_PUBLICA", nullable=True)
    dados_processo_id: Mapped[UUID] = mapped_column(ForeignKey("DADOS_PROCESSOS.ID"))

    dados_processo: Mapped["DadosProcesso"] = relationship(back_populates="informacoes_adicionais")

Base.metadata.create_all(engine)