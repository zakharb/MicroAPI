"""
    MicroAPI
    DB module for order-service
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
        Make engine, connection to DB and tables
"""

import os
import sqlalchemy

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = sqlalchemy.create_engine(DATABASE_URI)
metadata = sqlalchemy.MetaData()

orders = sqlalchemy.Table(
    'orders',
    metadata,
    sqlalchemy.Column('order_id', sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column('order_no', sqlalchemy.BigInteger),
    sqlalchemy.Column('customer_id', sqlalchemy.BigInteger),
    sqlalchemy.Column('product_id', sqlalchemy.BigInteger),
    sqlalchemy.Column('quantity', sqlalchemy.BigInteger),
    sqlalchemy.Column('price_net', sqlalchemy.Integer),
    sqlalchemy.Column('price_gross', sqlalchemy.Integer),
)

database = Database(DATABASE_URI)