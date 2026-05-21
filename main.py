import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Backend Modular de IA")

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "mi_secreto_123")

@app.get("/")
def inicio():
    return {"status": "Servidor corriendo en Windows 11"}

# Endpoint para que Meta valide que tu servidor existe en internet
@app.get("/webhook")
def verificar_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: int = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=str(hub_challenge))
    raise HTTPException(status_code=403, detail="Token inválido")

# Endpoint donde llegarán las conversaciones de WhatsApp
@app.post("/webhook")
async def recibir_mensaje(datos: dict):
    print("--- MENSAJE ENTRANTE ---")
    print(datos)
    return {"status": "recibido"}