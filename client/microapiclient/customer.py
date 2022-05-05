"""
    MicroAPI
    Module for communication with CustomerAPI
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

    Description:

    Author:
        Bengart Zakhar

"""
import json
import aiohttp
import logging
from datetime import datetime


class Customer:
    """
    Class for work with CustomerAPI
    """
    def __init__(self):
        self.url = "http://localhost:8080/api/v1/customers/"
        self.session = aiohttp.ClientSession()

    async def get_customers(self):
        """
        Get data about all customers
        """
        try:
            async with self.session.get(self.url, timeout=1) as resp:
                if resp.status != 200:
                    logging.error('CustomerAPI getting resp error, code: ' + str(resp.status))
                    return
                return await resp.text()
        except Exception as e:
            logging.error('CustomerAPI getting data error: ' + repr(e))

    async def get_customer(self, customer_id):
        """
        Get data about customer by ID
        """
        try:
            url = self.url + customer_id + '/'
            async with self.session.get(url, timeout=1) as resp:
                if resp.status != 200:
                    logging.error('CustomerAPI getting resp error, code: ' + str(resp.status))
                    return '{}'
                return await resp.text()
        except Exception as e:
            logging.error('CustomerAPI getting data error: ' + repr(e))

    async def post_customer(self, data):
        """
        Post new Customer into DB
        """
        try:
            headers = {
                'content-type': 'application/json',
            }
            pload = json.dumps(data, default=str, ensure_ascii=False)
            async with self.session.post(self.url, data=pload, headers=headers, timeout=1) as resp:
                if resp.status != 201:
                    logging.error('CustomerAPI posting response code: ' + str(resp.status))
                return await resp.text()
        except Exception as e:
            logging.error('CustomerAPI posting data error: ' + repr(e))

    async def close_session(self):
        await self.session.close()