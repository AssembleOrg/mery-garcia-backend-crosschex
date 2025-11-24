from fastapi import FastAPI
from routers import attendance 

app = FastAPI(
    title="API CrossChex Integration",
    description="API para consultar horas trabajadas",
    version="1.0.0"
)

app.include_router(attendance.router)

@app.get("/")
def read_root():
    return {"mensaje": "La API está funcionando correctamente"}