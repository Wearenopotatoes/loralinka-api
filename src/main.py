from typing import Union

from fastapi import FastAPI
from src.features.users.controller import router as users_router
from src.features.catalogs.controller import router as catalogs_router
from src.features.emergencies.controller import router as emergencies_router

app = FastAPI(
    title="Loralink API",
    version="0.1.0",
    description="API de de registro de emergencias LoraLink.",
)

# Registrar routers de features para exponer endpoints y documentarlos
app.include_router(users_router)
app.include_router(catalogs_router)
app.include_router(emergencies_router)
