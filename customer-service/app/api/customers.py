"""
    MicroAPI
    Routers for customer-service
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
        Routers for operations with API
"""

from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import CustomerOut, CustomerIn, CustomerUpdate
from app.api import db_manager

from datetime import datetime
router = APIRouter()

@router.post('/', response_model=CustomerOut, status_code=201)
async def create_customer(payload: CustomerIn):
    customer_id = await db_manager.add_customer(payload)
    response = {
        'customer_id': customer_id,
        **payload.dict()
    }
    return response

@router.get('/', response_model=List[CustomerOut])
async def get_customers():
    return await db_manager.get_all_customers()

@router.get('/{customer_id}/', response_model=CustomerOut)
async def get_customer(customer_id: int):
    customer = await db_manager.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put('/{customer_id}/', response_model=CustomerOut)
async def update_customer(customer_idid: int, payload: CustomerUpdate):
    customer = await db_manager.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = payload.dict(exclude_unset=True)
    customer_in_db = CustomerIn(**customer)
    updated_customer = customer_in_db.copy(update=update_data)
    return await db_manager.update_customer(customer_id, updated_customer)

@router.delete('/{customer_id}', response_model=None)
async def delete_customer(customer_id: int):
    customer = await db_manager.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return await db_manager.delete_customer(customer_id)
