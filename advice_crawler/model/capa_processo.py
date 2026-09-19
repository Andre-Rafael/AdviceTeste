from datetime import datetime
from uuid import uuid1, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .dados_processo import DadosProcesso
from .base import Base, engine

class CapaProcesso(Base):
    __tablename__ = "CAPA_PROCESSO"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid1, name='ID')
    process_number: Mapped[str] = mapped_column(name="NUMERO_DO_PROCESSO")
    data_autuacao: Mapped[datetime] = mapped_column(name="DATA_AUTUACAO")
    situacao: Mapped[str] = mapped_column(name="SITUACAO")
    orgao_julgador: Mapped[str] = mapped_column(name="ORGAO_JULGADOR")
    juiz: Mapped[str] = mapped_column(name="JUIZ")
    classe_acao: Mapped[str] = mapped_column(name="CLASSE_ACAO")
    dados_processo_id: Mapped[UUID] = mapped_column(ForeignKey("DADOS_PROCESSOS.ID"))

    dados_processo: Mapped["DadosProcesso"] = relationship(back_populates="capas_processo")

Base.metadata.create_all(engine)