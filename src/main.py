from typing import Union

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from src.features.users.controller import router as users_router
from src.features.catalogs.controller import router as catalogs_router
from src.features.emergencies.controller import router as emergencies_router
from src.features.emergency_units.controller import router as emergency_units_router
from src.auth.dependencies import verify_api_key
from src.auth.rate_limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from scalar_fastapi import get_scalar_api_reference
app = FastAPI(
    title="Loralink API",
    version="0.1.0",
    description="API de de registro de emergencias LoraLink.",
    docs_url=None,
    redoc_url=None
)

# Add CORS middleware for documentation UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000", "http://loralink.live"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Registrar routers de features para exponer endpoints y documentarlos
app.include_router(users_router, dependencies=[Depends(verify_api_key)])
app.include_router(catalogs_router, dependencies=[Depends(verify_api_key)])
app.include_router(emergencies_router, dependencies=[Depends(verify_api_key)])
app.include_router(emergency_units_router, dependencies=[Depends(verify_api_key)])

# Add a route to display the Scalar documentation UI
@app.get("/scalar", include_in_schema=False)
@limiter.limit("10/minute")
async def scalar_html(request: Request):
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )