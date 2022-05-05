"""
    MicroAPI
    Manager to work with DB at customer-service
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

from app.api.models import CustomerIn, CustomerOut, CustomerUpdate
from app.api.db import customers, database


async def add_customer(payload: CustomerIn):
    query = customers.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_customers():
    query = customers.select()
    return await database.fetch_all(query=query)

async def get_customer(customer_id):
    query = customers.select(customers.c.customer_id==customer_id)
    return await database.fetch_one(query=query)

async def delete_customer(customer_id: int):
    query = customers.delete().where(customers.c.customer_id==customer_id)
    return await database.execute(query=query)

async def update_customer(customer_id: int, payload: CustomerIn):
    query = (
        customers
        .update()
        .where(customers.c.customer_id == customer_id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)