from typing import List
from uuid import uuid1, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, engine


class DadosProcesso(Base):
    __tablename__ = "DADOS_PROCESSOS"
    id: Mapped[UUID] = mapped_column(primary_key=True, name="ID", default=uuid1)
    name: Mapped[str] = mapped_column(name="NOME_ENVOLVIDO")

    atualizacoes: Mapped[List["Atualizacoes"]] = relationship(
        back_populates="dados_processo",
        cascade="all"
    )
    assuntos: Mapped[List["Assunto"]] = relationship(
        back_populates="dados_processo",
        cascade="all"
    )
    capas_processo: Mapped[List["CapaProcesso"]] = relationship(
        back_populates="dados_processo",
        cascade="all"
    )
    partes_representantes: Mapped[List["PartesRepresentantes"]] = relationship(
        back_populates="dados_processo",
        cascade="all"
    )
    informacoes_adicionais: Mapped[List["InformacaoAdicional"]] = relationship(
        back_populates="dados_processo",
        cascade="all"
    )

Base.metadata.create_all(engine)