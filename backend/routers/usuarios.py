from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(
    prefix='/usuarios',  
    tags=['usuarios'] 
)

@router.post('/', response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail='Email já registrado')
    return crud.create_usuario(db=db, usuario=usuario)

@router.get('/{usuario_id}', response_model=schemas.Usuario)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return db_usuario
