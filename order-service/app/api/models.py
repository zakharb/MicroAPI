"""
    MicroAPI
    Models to order-service
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
        Pydantic models to make docs and check types
"""

from pydantic import BaseModel
from typing import List, Optional


class OrderIn(BaseModel):
    order_no: int
    customer_id: int
    product_id: int
    quantity: int
    price_net: int
    price_gross: int


class OrderOut(OrderIn):
    order_id: int


class OrderUpdate(OrderIn):
    customer_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    price_net: Optional[int] = None
    price_gross: Optional[int] = None
