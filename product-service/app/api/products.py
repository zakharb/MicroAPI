"""
    MicroAPI
    Routers for product-service
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

from typing import List, Optional
from fastapi import APIRouter, HTTPException

from app.api.models import ProductOut, ProductIn, ProductUpdate
from app.api import db_manager

router = APIRouter()

@router.post('/', response_model=ProductOut, status_code=201)
async def create_product(payload: ProductIn):
    product_id = await db_manager.add_product(payload)
    response = {
        'product_id': product_id,
        **payload.dict()
    }
    return response

@router.get('/', response_model=List[ProductOut])
async def get_products(name: Optional[str] = None, status: Optional[str] = None):
    return await db_manager.get_all_products(name, status)

@router.get('/{id}/', response_model=ProductOut)
async def get_product(id: int):
    product = await db_manager.get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put('/{id}/', response_model=ProductOut)
async def update_product(id: int, payload: ProductUpdate):
    product = await db_manager.get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = payload.dict(exclude_unset=True)
    product_in_db = ProductIn(**product)
    updated_product = product_in_db.copy(update=update_data)
    return await db_manager.update_product(id, updated_product)

@router.delete('/{id}', response_model=None)
async def delete_product(id: int):
    product = await db_manager.get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return await db_manager.delete_product(id)
