import os
import asyncio
from selenium import webdriver
import time
from datetime import datetime
import asyncio
import aiohttp


async def generate(url, sleep):
    print(f'start:{datetime.now()}')
    await asyncio.sleep(sleep)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            http_content = await res.text()
            return http_content[0:100]


async def test():
    task1 = asyncio.create_task(generate('https://baidu.com', 1))
    task2 = asyncio.create_task(generate('http://sina.com', 5))

    result = await asyncio.gather(task1, task2, return_exceptions=True)
    print(f'end:{datetime.now()}')
    print(result)


if __name__ == '__main__':
    asyncio.run(test())
