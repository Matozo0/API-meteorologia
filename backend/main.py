from fastapi import FastAPI
from .routers import usuarios, dispositivos, medicoes

api = FastAPI()

app.include_router(usuarios.router)
app.include_router(dispositivos.router)
app.include_router(medicoes.router)