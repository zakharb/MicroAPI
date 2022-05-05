"""
    MicroAPI
	Manager to work with Micro API actions
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
        Manager is used to make some complex action with different services^
            - bulk write Orders
            - generate Orders to CSV file

"""
import json
import asyncio
import logging
from datetime import datetime
from random import randrange, choice

from .customer import Customer
from .product import Product
from .price import Price
from .order import Order

async def post_orders(file, task_number):
    """
    Bulk write orders to DB from CSV file
    """
    loop = asyncio.get_event_loop()
    time = datetime.now()
    with open(file, 'r') as f:
        raw_data = f.read().splitlines()
    tasks = []
    orders = []
    for data in raw_data[1:]:
        order = data.split(',')
        orders.append(order)
    order_count = len(orders) // task_number
    order_trash = len(orders) % task_number
    start_order = 0
    end_order = start_order + order_count + order_trash
    for i in range(task_number):
        print('Start task: ', i)
        task_order = orders[ start_order : end_order + 1]
        task = loop.create_task(task_post_orders(task_order))
        tasks.append(task)
        start_order = end_order
        end_order = start_order + order_count
    for task in tasks:
        await task
    print('Finished, time: ', datetime.now() - time)

async def task_post_orders(data):
    """
    Simple task to write Orders to DB
    """
    customer = Customer()
    product = Product()
    price = Price()
    db_order = Order()
    orders = []
    for d in data:
        order = {}
        response = await customer.get_customer(d[1])
        if response:
            customer_data = json.loads(response)
        else:
            continue
        if customer_data['status'] == 'Deleted':
            logging.warning('Customer status is Deleted: ' + customer_data['name'])
        parameters = '?name=' + d[2]
        response = await product.get_products(parameters)
        if response:
            product_data = json.loads(response)
        else:
            continue
        if product_data:
            product_data = product_data[0]
        else:
            logging.error('Product is Unknown: ' + d[2])
            continue
        if product_data['status'] == 'Inactive':
            logging.warning('Product status is Inactive: ' + product_data['name'])
        parameters = ('?quantity=' + str(d[3]) + 
                      '&price_net=' + str(product_data['price_net']) +
                      '&vat_percentage=' + str(customer_data['vat_percentage']) +
                      '&customer_class=' + customer_data['customer_class'])
        response = await price.get_price(parameters)
        price_data = json.loads(response)
        if not price_data:
            continue
        order['order_no'] = d[0]
        order['customer_id'] = customer_data['customer_id']
        order['product_id'] = product_data['product_id']
        order['quantity'] = d[3]
        order['price_net'] = price_data['price_net']
        order['price_gross'] = price_data['price_gross']
        await db_order.post_order(order)
    await customer.close_session()
    await product.close_session()
    await price.close_session()
    await db_order.close_session()

async def generate_orders(count, task_number):
    """
    Generate random Orders and save it to CSV file
    """
    order_count = count / task_number
    loop = asyncio.get_event_loop()
    time = datetime.now()
    tasks = []
    orders = []
    for i in range(task_number):
        print('Start task: ', i)
        task = loop.create_task(task_generate_orders(order_count))
        tasks.append(task)
    for task in tasks:
        orders += await task
    if orders:
        with open('orders.csv', 'w') as f:
            row = ''
            for data in orders[0]:
                row += str(data) + ','
            f.write(row + '\n')
            for order in orders:
                row = ''
                for data in order.values():
                    row += str(data) + ','
                f.write(row + '\n')
    print('Finished, time: ', datetime.now() - time)

async def task_generate_orders(order_count):
    """
    Simple task to generate Orders
    """
    i = 0
    customer = Customer()
    product = Product()
    price = Price()
    response = await customer.get_customers()
    count_customers = len(json.loads(response))
    response = await product.get_products()
    count_products = len(json.loads(response))
    orders = []
    while order_count > 0:
        order = {'order_no': randrange(100000)}
        response = await customer.get_customer(str(randrange(count_customers)))
        customer_data = json.loads(response)
        if not customer_data:
            order_count -= 1
            continue
        order['customer_id'] = customer_data['customer_id']
        response = await product.get_product(str(randrange(count_products)))
        product_data = json.loads(response)
        if not product_data:
            order_count -= 1
            continue
        order['product_name'] = product_data['name']
        if order_count % 10 == 0:
            order['product_name'] += 'unknown'
        order['quantity'] = str(randrange(60))
        orders.append(order)
        order_count -= 1
    await customer.close_session()
    await product.close_session()
    await price.close_session()
    return orders
