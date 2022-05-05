"""
    MicroAPI
    Routers for price-service
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

from app.api.models import PriceIn, PriceOut

router = APIRouter()


def rebate_class(price, customer_class):
    if customer_class == "Reseller":
        price *= 0.95
    elif customer_class == "ResellerHighVolume":
        price *= 0.93
    return price

def rebate_quantity(price, quantity):
    if quantity > 50:
        price *= 0.98
    elif quantity > 10:
        price *= 0.99
    return price

@router.get('/', response_model=PriceOut)
async def get_price(quantity: int,
                    price_net: int, 
                    vat_percentage: int, 
                    customer_class: str):
    price_net = rebate_class(price_net, customer_class)
    price_net = rebate_quantity(price_net, quantity)
    price_net *= quantity
    price_gross = price_net * (1 + vat_percentage / 100)
    response = {
        "price_net": price_net,
        "price_gross": price_gross
    }
    return response
