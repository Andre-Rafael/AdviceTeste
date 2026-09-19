from uuid import UUID, uuid1

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, engine
from .dados_processo import DadosProcesso


class Assunto(Base):
    __tablename__ = "ASSUNTO"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid1, name='ID')
    codigo: Mapped[str] = mapped_column(name="CODIGO")
    descricao: Mapped[str] = mapped_column(name="DESCRICAO")
    principal: Mapped[bool] = mapped_column(name="PRINCIPAL")
    dados_processo_id: Mapped[UUID] = mapped_column(ForeignKey("DADOS_PROCESSOS.ID"))

    dados_processo: Mapped["DadosProcesso"] = relationship(back_populates="assuntos")

Base.metadata.create_all(engine)