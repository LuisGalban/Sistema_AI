# Sistema_AI - SaaS Multi-tenant & Asistente IA para WhatsApp

Backend modular desarrollado con **FastAPI** que integra la API Cloud oficial de **Meta WhatsApp Business** con el modelo **Google Gemini** para ofrecer atención al cliente automatizada, con memoria contextual por usuario y reglas estrictas de comportamiento (*System Instructions*).

---

## 🚀 Características Clave

- **Integración con Meta WhatsApp Cloud API**: Webhook optimizado para recibir y responder mensajes de texto en tiempo real mediante peticiones asíncronas HTTPX.
- **Memoria de Conversación por Usuario**: Mantenimiento de sesiones de chat individuales para conservar el contexto y la continuidad de la interacción.
- **Riesgo Cero de Alucinación**: Configuración de temperatura baja (0.2) e instrucciones de sistema que limitan las respuestas strictly al contexto corporativo provisto.
- **Arquitectura Limpia y Modular**: Enrutamiento mediante `APIRouter` de FastAPI, separación de servicios de IA y gestión segura de variables de entorno con `python-dotenv`.

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Integración IA:** Google GenAI SDK (`google-genai`)
- **HTTP Client:** HTTPX
- **Integración de Mensajería:** Meta WhatsApp Business Cloud API

---

## 📁 Estructura del Proyecto

```text
Sistema_AI/
├── app/
│   ├── routes/
│   │   └── webhook.py       # Endpoints para verificación y procesamiento de Meta
│   └── services/
│       └── ia_service.py    # Lógica de Gemini SDK, sesiones y prompts
├── .env.example              # Plantilla de variables de entorno
├── main.py                   # Punto de entrada de la aplicación FastAPI
└── requirements.txt          # Dependencias del proyecto
```

---

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/LuisGalban/Sistema_AI.git](https://github.com/LuisGalban/Sistema_AI.git)
   cd Sistema_AI
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno (`.env`):**
   Crea un archivo `.env` en la raíz del proyecto basado en las variables requeridas:
   ```env
   GOOGLE_API_KEY=tu_google_api_key
   WHATSAPP_VERIFY_TOKEN=tu_token_de_verificacion
   WHATSAPP_ACCESS_TOKEN=tu_meta_access_token
   WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
   ```

5. **Ejecutar el servidor:**
   ```bash
   uvicorn main:app --reload
   ```

La API estará disponible en `http://127.0.0.1:8000` y la documentación interactiva Swagger UI en `http://127.0.0.1:8000/docs`.
