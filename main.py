from fastapi import FastAPI
from app.api import chat
from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base  # Update this import
from app.api import nasaApi


app = FastAPI(title=settings.PROJECT_NAME)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(nasaApi.router, prefix="/api/Prediction", tags=["Prediction Model"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)