import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
import Auth
import staticfile as static

# async def middleware_factory(app, handler):
#     async def middleware_handler(request):        
#         return await handler(request)
#     return sss

async def logout(request): 
    data={}
    data['title']='登录' 
    data['main']=static.assets
    res = aiohttp_jinja2.render_template('login.jinja2',
                                              request,
                                              data)
    res.set_cookie('uid','logout')
    return res
    
async def login(request): 
    data={}
    data['title']='登录' 
    data['main']=static.assets
    res = aiohttp_jinja2.render_template('loging.jinja2',
                                              request,
                                              data)
    res.set_cookie('uid','xhzbglyxgs')
    return res

app = web.Application(middlewares=[Auth.middleware_factory])
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('./view'))

app.router.add_route('GET', '/', Auth.loginPage)
app.router.add_route('POST', '/login', login)
app.router.add_route('POST','/logout', logout)
app.router.add_static('/static/', './bower_components')
app.router.add_static('/pitures/', './public')
web.run_app(app)