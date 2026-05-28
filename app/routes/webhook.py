import os
import httpx
from fastapi import APIRouter, Request, Query, HTTPException, status
from app.services.ia_service import procesar_con_ia

router = APIRouter()

TOKEN_VERIFICACION = os.getenv("WHATSAPP_VERIFY_TOKEN", "luis_prueba_segura_123")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

def enviar_mensaje_whatsapp(telefono_destino: str, texto_respuesta: str):
    """
    Función que dispara el mensaje de vuelta al WhatsApp del usuario
    usando la API oficial de Meta Cloud.
    """
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": telefono_destino,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": texto_respuesta
        }
    }
    
    # Disparar la petición síncrona a Meta
    with httpx.Client() as client:
        response = client.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✉️ Mensaje enviado con éxito a {telefono_destino}")
        else:
            print(f"❌ Error al enviar mensaje a Meta: {response.status_code} - {response.text}")


@router.get("/webhook/empresa_a")
def verificar_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: int = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == TOKEN_VERIFICACION:
        print("✅ Webhook verificado exitosamente por Meta.")
        return hub_challenge
    raise HTTPException(status_code=403, detail="Token inválido.")


@router.post("/webhook/empresa_a")
async def recibir_mensaje_whatsapp(request: Request):
    try:
        payload = await request.json()
        
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", "")
        
        if "messages" in value:
            mensaje = value["messages"][0]
            contacto = value["contacts"][0]
            
            nombre_usuario = contacto.get("profile", {}).get("name", "Usuario")
            mensaje_usuario = mensaje.get("text", {}).get("body", "")
            telefono_usuario = mensaje.get("from", "") 
            
            print(f"\n--- 📱 MENSAJE ENTRANTE DESDE WHATSAPP ---")
            print(f"De: {nombre_usuario} ({telefono_usuario}) | Mensaje: {mensaje_usuario}")
            
            # 1. Procesar con Gemini y extraer la respuesta
            respuesta_bot = procesar_con_ia(telefono_usuario, mensaje_usuario)
            print(f"🤖 Respuesta de Gemini: {respuesta_bot}")
            
            # 2. 🔥 ¡EL PASO CLAVE! Enviar la respuesta directo al teléfono del usuario
            enviar_mensaje_whatsapp(telefono_usuario, respuesta_bot)
            
            return {"status": "recibido"}
            
        return {"status": "evento_no_mensajeria"}

    except Exception as e:
        print(f"❌ Error procesando el webhook de Meta: {str(e)}")
        return {"status": "error", "detail": str(e)}