from typing import Union

from fastapi import FastAPI
from src.features.users.controller import router as users_router

# Import opcional del router de emergencias si existe
try:
    from src.features.emergencies.controller import router as emergencies_router  # type: ignore
except Exception:  # pragma: no cover
    emergencies_router = None  # type: ignore

app = FastAPI(
    title="Loralinka API",
    version="0.1.0",
    description="API de ejemplo con módulos y routers registrados.",
)

# Registrar routers de features para exponer endpoints y documentarlos
app.include_router(users_router)
if emergencies_router:
    app.include_router(emergencies_router)
