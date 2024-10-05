# NASA Análisis API

Esta API permite hacer predicciones meteorológicas basadas en datos de observación de la Tierra, proporcionando métricas clave como temperatura, precipitación, velocidad del viento y humedad relativa.

## Parámetros de Interés:

- **`T2M`**: Temperatura a 2 metros (°C)
- **`PRECTOT`**: Precipitación total (mm/día)
- **`WS10M`**: Velocidad del viento a 10 metros (m/s)
- **`RH2M`**: Humedad relativa a 2 metros (%)

## Requisitos Previos:

- **Python 3.8+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic** (para migraciones de base de datos)

## Estructura del Proyecto:

```bash
chatbot_api/
│
├── alembic/              # Para migraciones de base de datos
│   └── versions/
│
├── app/
│   ├── api/              # "Vista" en MVC (endpoints de FastAPI)
│   │   ├── __init__.py
│   │   ├── chat.py       # Endpoints relacionados con el chat
│   │
│   ├── core/             # Configuraciones centrales
│   │   ├── __init__.py
│   │   ├── config.py     # Configuraciones de la aplicación
│   │   └── security.py   # Funciones relacionadas con seguridad
│   │
│   ├── db/               # Configuración de la base de datos
│   │   ├── __init__.py
│   │   └── session.py    # Sesión de SQLAlchemy
│   │
│   ├── models/           # "Modelo" en MVC (modelos SQLAlchemy)
│   │   ├── __init__.py
│   │   └── chat.py       # Modelo para mensajes de chat
│   │
│   ├── schemas/          # Esquemas Pydantic para validación de datos
│   │   ├── __init__.py
│   │   └── chat.py       # Esquemas para datos de chat
│   │
│   ├── services/         # "Controlador" en MVC (lógica de negocio)
│   │   ├── __init__.py
│   │   ├── chat.py       # Lógica para manejo de chats
│   │   └── whatsapp.py   # Lógica para interacción con WhatsApp
│   │
│   ├── dao/              # Data Access Objects
│   │   ├── __init__.py
│   │   └── chat.py       # DAO para operaciones de chat en la BD
│   │
│   └── utils/            # Utilidades generales
│       ├── __init__.py
│       └── weather.py    # Utilidad para obtener datos del clima
│
├── tests/                # Pruebas unitarias y de integración
│   ├── __init__.py
│   ├── test_api/
│   └── test_services/
│
├── .env                  # Variables de entorno (no versionar)
├── .gitignore
├── alembic.ini           # Configuración de Alembic
├── main.py               # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias del proyecto
└── README.md
```

## Ejecutar la API en Desarrollo:
Para ejecutar la API en modo desarrollo, utiliza el siguiente comando:

```bash
uvicorn main:app --reload
```

## Uso de Docker:
Para construir y ejecutar la aplicación con Docker, sigue estos pasos:

### Construir la Imagen:

```bash
docker build -t nasa-analisis-api .
```

### Ejecutar el Contenedor:
```bash
docker run -p 8000:8000 nasa-analisis-api
```
