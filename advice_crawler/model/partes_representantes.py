from uuid import uuid1, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .dados_processo import DadosProcesso
from .base import Base, engine

class PartesRepresentantes(Base):
    __tablename__ = "PARTES_REPRESENTANTES"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid1, name='ID')
    titulo: Mapped[str] = mapped_column(name="TITULO")
    nome: Mapped[str] = mapped_column(name="NOME")
    dados_processo_id: Mapped[UUID] = mapped_column(ForeignKey("DADOS_PROCESSOS.ID"))

    dados_processo: Mapped["DadosProcesso"] = relationship(back_populates="partes_representantes")

Base.metadata.create_all(engine)