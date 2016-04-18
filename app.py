import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
import Auth

# async def middleware_factory(app, handler):
#     async def middleware_handler(request):        
#         return await handler(request)
#     return sss

async def logout(req):
    res=web.Response()
    res.set_cookie('uid','logout')
    res.headers['Request-url']= '/'
    return res
    pass

async def hello(request):    
    return web.Response(body=b"Hello, world")

app = web.Application(middlewares=[Auth.middleware_factory])
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('./view'))

app.router.add_route('GET', '/', Auth.login)
app.router.add_route('GET', '/auth', hello)
app.router.add_route('GET','/logout', logout)
app.router.add_static('/static/', './bower_components')
web.run_app(app)