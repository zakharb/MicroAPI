"""
    MicroAPI
    Models to customer-service
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

from pydantic import BaseModel, constr
from typing import List, Optional
from enum import Enum

class CustomerClassEnum(str, Enum):
    enduser = 'Enduser'
    reseller = 'Reseller'
    resseler_high_volume = 'ResellerHighVolume'


class Status(str, Enum):
    active = 'Active'
    deleted = 'Deleted'


class CustomerIn(BaseModel):
    name: str
    customer_class: CustomerClassEnum
    vat_percentage: int
    status: Status


class CustomerOut(CustomerIn):
    customer_id: int


class CustomerUpdate(CustomerIn):
    name: Optional[str] = None
    customer_class: Optional[CustomerClassEnum] = None
    vat_percentage: Optional[int] = None
    status: Optional[Status] = None
