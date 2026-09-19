from datetime import datetime
from uuid import uuid1, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .dados_processo import DadosProcesso
from .base import Base, engine

class Atualizacoes(Base):
    __tablename__ = "ATUALIZACOES"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid1, name='ID')
    ordem_evento: Mapped[str] = mapped_column(name="ORDEM_EVENTO")
    data_hora: Mapped[datetime] = mapped_column(name="DATA_HORA")
    descricao: Mapped[str] = mapped_column(name="DESCRICAO")
    usuario: Mapped[str] = mapped_column(name="USUARIO")
    documentos: Mapped[str] = mapped_column(name="DOCUMENTOS")
    dados_processo_id: Mapped[UUID] = mapped_column(ForeignKey("DADOS_PROCESSOS.ID"))

    dados_processo: Mapped["DadosProcesso"] = relationship(back_populates="atualizacoes")

Base.metadata.create_all(engine)