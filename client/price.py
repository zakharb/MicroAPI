"""
    MicroAPI
    Module for communication with PriceAPI
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
import aiohttp
import logging
from datetime import datetime


class Price:
    """
    Class for work with PriceAPI
    """
    def __init__(self):
        self.url = "http://localhost:8080/api/v1/prices/"
        self.session = aiohttp.ClientSession()

    async def get_price(self, parameters):
        """
        Get data about prices with parameters by Name or Status
        """
        try:
            if parameters:
                url = self.url + parameters
            async with self.session.get(url, timeout=1) as resp:
                if resp.status != 200:
                    logging.error('PriceAPI getting resp error, code: ' + str(resp.status))
                return await resp.text()
        except Exception as e:
            logging.error('PriceAPI getting data error: ' + repr(e))

    async def close_session(self):
        await self.session.close()