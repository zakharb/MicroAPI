"""
    MicroAPI
    Manager to work with DB at order-service
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

from app.api.models import OrderIn, OrderOut, OrderUpdate
from app.api.db import orders, database


async def add_order(payload: OrderIn):
    query = orders.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_orders():
    query = orders.select()
    return await database.fetch_all(query=query)

async def get_order(id):
    query = orders.select(orders.c.id==id)
    return await database.fetch_one(query=query)

async def delete_order(id: int):
    query = orders.delete().where(orders.c.id==id)
    return await database.execute(query=query)

async def update_order(id: int, payload: OrderIn):
    query = (
        orders
        .update()
        .where(orders.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)