import asyncio
from datetime import datetime as dt
from aiohttp import web
import staticfile as static
import aiohttp_jinja2

users={'uid':'xhzb','psw':'xhzbglyxgs'}

@aiohttp_jinja2.template('login.jinja2')
async def loginPage(request):
    data={}
    data['title']='登录' 
    data['main']=static.assets
    data['question']='密码前5位是：'    
       
    return data
    pass



async def middleware_factory(app, handler):
    async def middleware_handler(req):
        # if req.path == '/' or req.path.startswith('/static/')\
        #         or req.cookies.get('uid') == users['psw']:
        if req.path.startswith('/pitures/') and \
        req.cookies.get('uid') != users['psw']:
            #assert(req.cookies.get('uid')==users['psw'])
            print(req.cookies.get('uid'))
            return web.HTTPFound('/')
            
        else: 
            return await handler(req)
            pass
                
    return middleware_handler