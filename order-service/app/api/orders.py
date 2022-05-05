"""
    MicroAPI
    Routers for order-service
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

from app.api.models import OrderOut, OrderIn, OrderUpdate
from app.api import db_manager

router = APIRouter()

@router.post('/', response_model=OrderOut, status_code=201)
async def create_order(payload: OrderIn):
    order_id = await db_manager.add_order(payload)
    response = {
        'order_id': order_id,
        **payload.dict()
    }
    return response

@router.get('/', response_model=List[OrderOut])
async def get_orders():
    return await db_manager.get_all_orders()

@router.get('/{id}/', response_model=OrderOut)
async def get_order(id: int):
    order = await db_manager.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put('/{id}/', response_model=OrderOut)
async def update_order(id: int, payload: OrderUpdate):
    order = await db_manager.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    update_data = payload.dict(exclude_unset=True)
    order_in_db = OrderIn(**order)
    updated_order = order_in_db.copy(update=update_data)
    return await db_manager.update_order(id, updated_order)

@router.delete('/{id}', response_model=None)
async def delete_order(id: int):
    order = await db_manager.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return await db_manager.delete_order(id)
