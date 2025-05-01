import asyncio
import aiohttp


async def inc(i):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://127.0.0.1:8000/inc/{i}') as response:
            return int(await response.read())


async def main(n):
    futures = [inc(i) for i in range(n)]
    result = await asyncio.gather(*futures)
    print(result)


if __name__ == '__main__':
    asyncio.run(main(64))
