from fastapi import FastAPI
from app.api.customers import router as customers_router
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/customers/openapi.json", 
              docs_url="/api/v1/customers/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(customers_router, prefix='/api/v1/customers', tags=['customers'])