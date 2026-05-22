import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from openai import AuthenticationError, RateLimitError

# Inicializamos el modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def procesar_con_ia(nombre_usuario: str, mensaje_usuario: str) -> str:
    """
    Función modular que intenta procesar el mensaje con OpenAI.
    Si falla la API Key, activa el plan de contingencia simulado.
    """
    try:
        instrucciones = SystemMessage(content="Eres un asistente de servicio al cliente amable y conciso.")
        mensaje = HumanMessage(content=mensaje_usuario)
        
        respuesta_ia = llm.invoke([instrucciones, mensaje])
        return respuesta_ia.content
        
    except (AuthenticationError, RateLimitError, Exception) as e:
        print(f"Aviso en servicio: OpenAI no disponible ({type(e).__name__}). Usando simulación.")
        return (
            f"¡Hola {nombre_usuario}! (Modo Simulado Activo). "
            f"Recibí tu pregunta: '{mensaje_usuario}'."
        )