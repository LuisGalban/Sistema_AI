from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import webhook # Importamos nuestro nuevo archivo de rutas

load_dotenv()

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