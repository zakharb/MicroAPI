from fastapi import FastAPI
from app.api.products import router as products_router
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/products/openapi.json", 
              docs_url="/api/v1/products/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(products_router, prefix='/api/v1/products', tags=['products'])