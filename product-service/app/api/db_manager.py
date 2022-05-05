"""
    MicroAPI
    Manager to work with DB at product-service
    Copyright (C) 2022

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Author:
        Bengart Zakhar

    Description:
        CRUD operations to work with DB
"""

from app.api.models import ProductIn, ProductOut, ProductUpdate
from app.api.db import products, database


async def add_product(payload: ProductIn):
    query = products.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_products(name, status):
    if name and status:
        query = products.select(products.c.name==name and products.c.status==status)
    elif name:
        query = products.select(products.c.name==name)
    elif status:
        query = products.select(products.c.status==status)
    else:
        query = products.select()
    return await database.fetch_all(query=query)

async def get_product(id):
    query = products.select(products.c.product_id==id)
    return await database.fetch_one(query=query)

async def delete_product(id: int):
    query = products.delete().where(products.c.product_id==id)
    return await database.execute(query=query)

async def update_product(id: int, payload: ProductIn):
    query = (
        products
        .update()
        .where(products.c.product_id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)