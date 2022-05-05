from fastapi import FastAPI
from app.api.prices import router as prices_router

app = FastAPI(openapi_url="/api/v1/prices/openapi.json", 
              docs_url="/api/v1/prices/docs")

app.include_router(prices_router, prefix='/api/v1/prices', tags=['prices'])