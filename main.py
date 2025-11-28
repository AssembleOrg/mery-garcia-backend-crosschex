from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import attendance 

app = FastAPI(
    title="API CrossChex Integration",
    description="API para consultar horas trabajadas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" permite que todos se puedan conectar
    allow_credentials=True,
    allow_methods=["*"],  # permite todos los metodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # permite todos los encabezados
)

app.include_router(attendance.router)

@app.get("/")
def read_root():
    return {"mensaje": "La API está funcionando correctamente"}