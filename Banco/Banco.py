# !/usr/bin/env python
# *- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer, Float, VARCHAR, Date
from Config.Config import Config

config = Config().config_banco
Base = declarative_base()

class Posto(Base):
    __tablename__ = 'tbl_posto'

    id = Column(Integer)
    num_usina = Column(Integer)
    num_posto = Column(Integer, primary_key=True)
    nom_usina = Column(VARCHAR(255))
    nom_posto = Column(VARCHAR(255))
    num_ordem = Column(Integer)
    num_jusante = Column(Integer)
    val_lat = Column(Float)
    val_lon = Column(Float)

    # Relações
    vazoes = relationship('Vazao', back_populates='posto')


class Vazao(Base):
    __tablename__ = 'tbl_vazao'

    id = Column(Integer, primary_key=True)
    num_posto = Column(Integer, ForeignKey('tbl_posto.num_posto'))
    dat_medicao = Column(Date)
    val_vaz_natr = Column(Float)
    val_vaz_defl = Column(Float)
    val_vaz_aflu = Column(Float)
    val_vaz_vert = Column(Float)
    val_vaz_incr = Column(Float)
    val_cota = Column(Float)

    # Relacoes
    posto = relationship('Posto', back_populates='vazoes')


class Chuva(Base):
    __tablename__ = 'tbl_chuva'

    id = Column(Integer, primary_key=True)
    val_lon = Column(Float)
    val_lat = Column(Float)
    dat_medicao = Column(Date)
    val_precip = Column(Float)

engine = create_engine(config['string_engine'].format(**config['credentials']))
Base.metadata.create_all(engine)

