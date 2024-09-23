from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
import jwt

SECRET_KEY = 'sarah'
ALGORITHM = 'HS256'

def verify_device_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        dispositivo_id: str = payload.get('sub')
        if dispositivo_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalido')
        db_dispositivo = db.query(models.Dispositivo).filter(models.Dispositivo.id == dispositivo_id).first()
        if db_dispositivo is None or db_dispositivo.token != token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalido')
        return db_dispositivo
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalido')

def create_device_token(dispositivo_id: int):
    to_encode = {'sub': dispositivo_id}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_dispositivos(db: Session, usuario_id: int):
    return db.query(models.Dispositivo).filter(models.Dispositivo.usuario_id == usuario_id).first()

def post_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hash_temporaria = usuario.hash_senha + 'abcteste123'
    db_usuario = models.Usuario(nome=usuario.nome, email=usuario.email, hash_senha=hash_temporaria)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def post_dispositvo(db: Session, dispositivo: schemas.DispositivoCreate, usuario_id: int):
    db_dispositivo = models.Dispositivo(nome=dispositivo.nome, usuario_id=usuario_id)
    token = create_device_token(db_dispositivo.id)
    db_dispositivo.token = token
    db.add(db_dispositivo)
    db.commit()
    db.refresh(db_dispositivo)
    return db_dispositivo

def post_medicao(db: Session, medicao: schemas.MedicaoCreate, usuario_id: int, dispositivo_id: int):
    db_medicao = models.Medicao(temperatura=medicao.temperatura, umidade=medicao.umidade, )
    db.add(db_medicao)
    db.commit()
    db.refresh(db_medicao)
    return db_medicao