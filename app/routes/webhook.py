import os
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse
from app.services.ia_service import procesar_con_ia

# Creamos el enrutador modular
router = APIRouter(prefix="/webhook", tags=["Webhook de WhatsApp"])

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
if not VERIFY_TOKEN:
    raise ValueError("Error crítico: No se encontró WHATSAPP_VERIFY_TOKEN en el archivo .env")

@router.get("")
def verificar_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: int = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=str(hub_challenge))
    raise HTTPException(status_code=403, detail="Token inválido")

@router.post("")
async def recibir_mensaje(datos: dict):
    print("\n--- NUEVO MENSAJE ENTRANTE (RUTA MODULAR) ---")
    try:
        mensaje_usuario = datos["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        nombre_usuario = datos["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
        
        texto_respuesta = procesar_con_ia(nombre_usuario, mensaje_usuario)
        
        return {
            "status": "procesado",
            "respuesta_generada": texto_respuesta
        }
    except KeyError:
        print("Aviso: Estructura de JSON no válida.")
        return {"status": "ignorado", "motivo": "Estructura no válida"}