import asyncio
from aiohttp import web

async def succeedregist(request): 
    text='ok.'
    para = await request.post()
    with open('registSucceed.txt','a',encode='utf-8') as f:
        f.write(para['name'])
    return web.Response(body=text.encode('utf-8'))