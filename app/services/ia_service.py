import os
from google import genai
from google.genai import types

# Inicializamos el cliente de Google (Busca GOOGLE_API_KEY en el .env)
client = genai.Client()

# --- BASE DE DATOS TEMPORAL DE HISTORIALES (MEMORIA) ---
# Guardará las sesiones de chat activas de cada usuario para mantener la continuidad.
# Estructura: {"Luis": objeto_chat_de_gemini, "Pedro": objeto_chat_de_gemini}
SESIONES_CHAT = {}

# --- BASE DE CONOCIMIENTOS REAL DE LA EMPRESA ---
# Esta es la única información que el bot conoce. Si no está aquí, NO puede inventar.
INFORMACION_EMPRESA = """
CONTEXTO GENERAL DE LA EMPRESA:
- Nombre: Soluciones Tech C.A.
- Servicios: Desarrollo de software a medida, automatización de procesos y consultoría tecnológica.
- Horario de atención: Lunes a Viernes de 8:00 AM a 5:00 PM.
- Canales de contacto: correo soporte@solucionestech.com.
- NOTA IMPORTANTE: No tenemos oficinas físicas de atención al público en este momento, todo es remoto.
"""

def obtener_o_crear_chat(nombre_usuario: str):
    """
    Si el usuario es nuevo, le crea un chat con memoria y su configuración.
    Si ya existe, devuelve su chat activo para continuar la conversación.
    """
    if nombre_usuario not in SESIONES_CHAT:
        print(f"🧠 Creando nueva memoria de chat para: {nombre_usuario}")
        
        # Definimos las reglas estrictas del bot (Instrucciones del Sistema)
        configuracion = types.GenerateContentConfig(
            system_instruction=(
                "Eres un asistente virtual corporativo profesional y amable.\n\n"
                f"REGLAS ABSOLUTAS DE COMPORTAMIENTO:\n"
                f"1. Usa EXCLUSIVAMENTE la siguiente información para responder:\n{INFORMACION_EMPRESA}\n"
                f"2. Si el usuario te pregunta por precios, direcciones, teléfonos o cualquier dato "
                f"que NO esté en el texto de arriba, debes responder exactamente: "
                f"'Disculpe, no dispongo de esa información en este momento. Permítame tomar sus datos "
                f"para que un asesor humano le contacte y le ayude.'\n"
                f"3. PROHIBIDO INVENTAR, deducir o alucinar datos (direcciones, calles, costos, etc.).\n"
                f"4. Mantén la continuidad del chat. Si ya saludaste al usuario al inicio, no vuelvas a "
                f"darle la bienvenida formal en los siguientes mensajes."
            ),
            temperature=0.2 # Bajamos la temperatura a 0.2 para que sea ultra preciso y menos creativo
        )
        
        # Creamos el objeto de chat con memoria nativa de Google
        SESIONES_CHAT[nombre_usuario] = client.chats.create(
            model="gemini-3.5-flash",
            config=configuracion
        )
        
    return SESIONES_CHAT[nombre_usuario]


def procesar_con_ia(nombre_usuario: str, mensaje_usuario: str) -> str:
    """
    Procesa el mensaje manteniendo la memoria del usuario y aplicando los filtros de verdad.
    """
    try:
        # 1. Recuperamos o creamos el historial de este usuario específico
        chat_activo = obtener_o_crear_chat(nombre_usuario)
        
        # 2. Enviamos el mensaje al chat (Gemini recuerda automáticamente lo anterior)
        response = chat_activo.send_message(mensaje_usuario)
        
        return response.text

    except Exception as e:
        print(f"Error crítico en el chat con memoria: {str(e)}")
        return (
            f"¡Hola {nombre_usuario}! Estamos experimentando un inconveniente técnico. "
            f"Un asesor se comunicará contigo pronto."
        )