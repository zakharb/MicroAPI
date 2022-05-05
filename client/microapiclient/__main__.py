"""
    MicroAPI
	Client to work with Micro API
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
        Client is used to manipulate with MicroAPI
        You can do CRUD operations with services
        It use Modules to every service and Manager wtih actions
        Work in Async mode with customized number of tasks
"""

import json
import asyncio
import logging
import argparse
from datetime import datetime

from random import randrange, choice
from logging.handlers import RotatingFileHandler
from microapiclient import Customer, Product, Price, Order
from microapiclient import post_orders, generate_orders

def print_logo():
    print('  __   __   _                      _____   _____  _______ \n'\
          ' (__)_(__) (_)        _           (_____) (_____)(_______)\n'\
          '(_) (_) (_) _    ___ (_)__  ___  (_)___(_)(_)__(_)  (_)   \n'\
          '(_) (_) (_)(_) _(___)(____)(___) (_______)(_____)   (_)   \n'\
          '(_)     (_)(_)(_)___ (_)  (_)_(_)(_)   (_)(_)     __(_)__ \n'\
          '(_)     (_)(_) (____)(_)   (___) (_)   (_)(_)    (_______)\n')

async def run_main(args):
    """
    Main function starting all tasks denends on args
    """
    if args.command == 'getcustomer':
        # get cutomer by ID from customer-service
        print('\n[*] Getting Customer by ID\n----------------')
        customer = Customer()
        data = await customer.get_customer(args.cid)
        print(data)
    elif args.command == 'postcustomer':
        # post random geretated Customers to DB
        print('\n[*] Posting new Customers\n----------------')
        customer = Customer()
        i = 0
        while args.customer_count > 0:
            data = {
                'name': 'Customer' + str(randrange(1000)),
                'customer_class': choice(['Enduser', 'Reseller', 'ResellerHighVolume']),
                'vat_percentage': str(randrange(30)),
                'status': choice(['Active', 'Deleted', 'Active', 'Active']),
            }
            response = await customer.post_customer(data)
            print(response)
            args.customer_count -= 1
        await customer.close_session()
    elif args.command == 'getproduct':
        # get products by Name and Status from product-service
        print('\n[*] Getting Product by name\n----------------')
        product = Product()
        parameters = ''
        if args.pname and args.pstatus:
            parameters += '?name=' + args.pname + '&' + 'status=' + args.pstatus
        elif args.pname:
            parameters += '?name=' + args.pname
        elif args.pstatus:
            parameters += '?status=' + args.pstatus
        data = await product.get_products(parameters)
        print(data)
        await product.close_session()
    elif args.command == 'postproduct':
        # post random geretated Products to DB
        print('\n[*] Posting new Products\n----------------')
        product = Product()
        i = 0
        while args.product_count > 0:
            data = {
                'name': 'Product' + str(randrange(100)),
                'price_net': str(randrange(300)),
                'status': choice(['Active', 'Inactive', 'Active', 'Active']),
            }
            response = await product.post_product(data)
            print(response)
            args.product_count -= 1
        await product.close_session()
    elif args.command == 'getprice':
        # calculate Price from price-service
        print('\n[*] Getting Price\n----------------')
        price = Price()
        parameters = ('?quantity=' + args.quantity + 
                      '&price_net=' + args.price_net +
                      '&vat_percentage=' + args.vat_percentage +
                      '&customer_class=' + args.customer_class)
        data = await price.get_price(parameters)
        print(data)
        await price.close_session()
    elif args.command == 'postorder':
        # post order with order-service 
        print('\n[*] Posting Order\n----------------')
        order = Order()
        data = {
            'order_no': args.order_no,
            'customer_id': args.customer_id,
            'product_id': args.product_id,
            'quantity': args.quantity,
            'price_net': args.price_net,
            'price_gross': args.price_gross,
        }
        response = await order.post_order(data)
        print(response)
        await order.close_session()
    elif args.command == 'postorders':
        # bulk write orders to DB from CSV file
        await post_orders(args.order_file, args.task_count)
    elif args.command == 'generateorder':
        # generate CSV file with orders
        await generate_orders(args.order_count, args.task_count)
    else:
        parser.print_help()


if __name__ == "__main__":
    """
    Use modelu Argparser to build menu with submenu
    """
    print_logo()
    logging.basicConfig(
        handlers=[RotatingFileHandler('client.log', maxBytes=1000000)],
        level='INFO',
        format=' %(asctime)s %(levelname)s %(message)s')
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    # args for Customer
    getcustomer = subparser.add_parser('getcustomer', help='Get customer from DB')
    getcustomer.add_argument('--cid', type=str, required=True, 
                             help='customer id')
    postcustomer = subparser.add_parser('postcustomer', 
                           help='Post new customer into DB')
    postcustomer.add_argument('--customer-count', type=int, required=True, 
                           help='how many customers to post')
    # args for Product
    getproduct = subparser.add_parser('getproduct', help='Get product by name from DB')
    getproduct.add_argument('--pname', type=str, 
                            help='product name')
    getproduct.add_argument('--pstatus', type=str, 
                            help='product status')
    postproduct = subparser.add_parser('postproduct', 
                           help='Post new product into DB')
    postproduct.add_argument('--product-count', type=int, required=True, 
                           help='how many products to post')
    # args for Price
    getprice = subparser.add_parser('getprice', help='Get price_net and price_gross')
    getprice.add_argument('--quantity', type=str, required=True, 
                          help='quantity of the product')
    getprice.add_argument('--price-net', type=str, required=True, 
                          help='price net')
    getprice.add_argument('--customer-class', type=str, required=True, 
                          help='customer class')
    getprice.add_argument('--vat-percentage', type=str, required=True, 
                          help='vat for product')
    # args for Order
    postorder = subparser.add_parser('postorder', help='Post order into DB')
    postorder.add_argument('--order-no', type=str, required=True, 
                           help='order number')
    postorder.add_argument('--customer-id', type=str, required=True, 
                           help='customer ID')
    postorder.add_argument('--product-id', type=str, required=True, 
                           help='product ID')
    postorder.add_argument('--quantity', type=str, required=True, 
                           help='amount to buy')
    postorder.add_argument('--price-net', type=str, required=True, 
                           help='net price')
    postorder.add_argument('--price-gross', type=str, required=True, 
                           help='gross price')
    # args for Manager actions
    postorders = subparser.add_parser('postorders', help='Post order into DB')
    postorders.add_argument('--order-file', type=str, required=True, 
                           help='file name to read orders')
    postorders.add_argument('--task-count', type=int, required=True, 
                           help='how many tasks to use')
    generateorder = subparser.add_parser('generateorder', 
                                         help='Generate order into CSV file')
    generateorder.add_argument('--order-count', type=int, required=True, 
                           help='how many orders to save')
    generateorder.add_argument('--task-count', type=int, required=True, 
                           help='how many tasks to use')

    args = parser.parse_args()
    asyncio.run(run_main(args))
