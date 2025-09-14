from typing import Union

from fastapi import FastAPI, Depends
from src.features.users.controller import router as users_router
from src.features.catalogs.controller import router as catalogs_router
from src.features.emergencies.controller import router as emergencies_router
from src.auth.dependencies import verify_api_key

from scalar_fastapi import get_scalar_api_reference
app = FastAPI(
    title="Loralink API",
    version="0.1.0",
    description="API de de registro de emergencias LoraLink.",
    docs_url=None,
    redoc_url=None
)

# Registrar routers de features para exponer endpoints y documentarlos
app.include_router(users_router, dependencies=[Depends(verify_api_key)])
app.include_router(catalogs_router, dependencies=[Depends(verify_api_key)])
app.include_router(emergencies_router, dependencies=[Depends(verify_api_key)])

# Add a route to display the Scalar documentation UI
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )