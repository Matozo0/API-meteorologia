from sqlalchemy import Column, Integer, Float, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from .database import Base

# Aqui contem os modelos que vão para o db usando SQLAlchemy

# Usuario.dispositivos.medicoes
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hash_senha = Column(String, nullable=False)
    token = Column(String,unique=True, nullable=False)

    # Define o Usuario como o dono do Dispositivo, ou seja, o Usuario herda dispositivo 
    dispositivos = relationship('Dispositivo', back_populates='dono')

class Dispositivo(Base):
    __tablename__ = 'dispositivos'
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    nome = Column(String, nullable=False, server_default=text('1'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    token = Column(String, nullable=False, unique=True)

    # Define o Dispositivo como o dono de Medicaoi, ou seja, o Dispositivo herda as medicoes
    medicoes = relationship('Medicao', back_populates='dono')
    # Define o dono como Usuario
    dono = relationship('Usuario', back_populates='dispositivos')

class Medicao(Base):
    __tablename__ = 'medicoes'  

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    temperatura = Column(Float, nullable=False, server_default=text('0'))
    umidade = Column(Float, nullable=False)
    dispositivo_id = Column(Integer, ForeignKey('dispositivos.id'))
    # Define o dono como Usuario
    dono = relationship('Dispositivo', back_populates='medicoes')