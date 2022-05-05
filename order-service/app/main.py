from fastapi import FastAPI
from app.api.orders import router as orders_router
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/orders/openapi.json", 
              docs_url="/api/v1/orders/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(orders_router, prefix='/api/v1/orders', tags=['orders'])