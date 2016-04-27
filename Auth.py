import asyncio
from datetime import datetime as dt
from aiohttp import web
import staticfile as static
import aiohttp_jinja2

users={'uid':'xhzb','psw':'xhzbglyxgs248'}
cookies={'Authentication':'JDKEJKjdkjgkjKDJJKjiei439954JKJDFK9482jkgKJDKjgijiKDJ394'}

@aiohttp_jinja2.template('login.jinja2')
async def loginPage(request):
    data={}
    data['title']='登录' 
    data['main']=static.assets           
    return data
    pass



async def middleware_factory(app, handler):
    async def middleware_handler(req):
        # if req.path == '/' or req.path.startswith('/static/')\
        #         or req.cookies.get('uid') == users['psw']:
        if req.path.startswith('/pitures/') and \
        req.cookies.get('Authentication') != cookies['Authentication']:            
            print(req.cookies.get('uid'))
            return web.HTTPFound('/')
            
        else: 
            print(req.path)
            return await handler(req)
            pass
                
    return middleware_handler