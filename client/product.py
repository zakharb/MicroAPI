"""
    MicroAPI
    Module for communication with ProductAPI
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
        Class to work with price-service

"""
import json
import aiohttp
import logging
from datetime import datetime


class Product:
    """
    Class for work with ProductAPI
    """
    def __init__(self):
        self.url = "http://localhost:8080/api/v1/products/"
        self.session = aiohttp.ClientSession()

    async def get_products(self, parameteres=None):
        """
        Get data about products with parameters by Name or Status
        """
        url = self.url
        if parameteres:
            url = self.url + parameteres
        try:
            async with self.session.get(url, timeout=1) as resp:
                if resp.status != 200:
                    logging.error('ProductAPI getting resp error, code: ' + str(resp.status))
                return await resp.text()
        except Exception as e:
            logging.error('ProductAPI getting data error: ' + repr(e))

    async def get_product(self, product_id):
        """
        Get data about product by ID
        """
        try:
            url = self.url + product_id + '/'
            async with self.session.get(url, timeout=1) as resp:
                if resp.status != 200:
                    logging.error('ProductAPI getting resp error, code: ' + str(resp.status))
                    return '{}'
                return await resp.text()
        except Exception as e:
            logging.error('ProductAPI getting data error: ' + repr(e))
    
    async def post_product(self, data):
        """
        Post new Product into DB
        """
        try:
            headers = {
                'content-type': 'application/json',
            }
            pload = json.dumps(data, default=str, ensure_ascii=False)
            async with self.session.post(self.url, data=pload, headers=headers, timeout=1) as resp:
                if resp.status != 201:
                    logging.error('ProductAPI posting response code: ' + str(resp.status))
                return await resp.text()
        except Exception as e:
            logging.error('ProductAPI posting data error: ' + repr(e))

    async def close_session(self):
        await self.session.close()