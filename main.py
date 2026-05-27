from fastapi import FastAPI
from dotenv import load_dotenv

# 1. CARGAR ENTORNO PRIMERO: Esto inyecta las llaves en memoria antes de que llamemos a los servicios
load_dotenv()

# 2. AHORA SÍ IMPORTAMOS LAS RUTAS: Cuando entre aquí, GOOGLE_API_KEY ya existirá en memoria
from app.routes import webhook 

app = FastAPI(
    title="Sistema_AI - Backend Modular",
    description="Plataforma SaaS multi-empresa para automatización de IA",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {"status": "Servidor corriendo con arquitectura limpia y modular"}

# Inyectamos las rutas del webhook en la aplicación principal
app.include_router(webhook.router)