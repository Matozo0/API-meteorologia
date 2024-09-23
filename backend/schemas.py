from pydantic import BaseModel
from typing import Optional

# Aqui contem os modelos para fazer validação dos tipos usando pydantic

class MedicaoBase(BaseModel):
    temperatura: int
    umidade: int

class MedicaoCreate(MedicaoBase):
    dispositivo_id: int

class Medicao(MedicaoBase):
    id: int
    timestamp: str
    dispositivo_id: int

    class Config:
        orm_mode = True


class DispositivoBase(BaseModel):
    nome: str

class DispositivoCreate(DispositivoBase):
    usuario_id: int

class Dispositivo(DispositivoBase):
    id: int
    usuario_id: int
    token: str
    medicoes: Optional[list[Medicao]] = []

    class Config:
        orm_mode = True


class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    hash_senha: str

class Usuario(UsuarioBase):
    id: int
    dispositivos: list[Dispositivo] = []

    class Config:
        orm_mode = True