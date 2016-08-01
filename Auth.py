import asyncio
from datetime import datetime as dt
from aiohttp import web
import staticfile as static
import aiohttp_jinja2

users={'uid':'xhzb','psw':'xhzb2015'}
cookies={'Authentication':'JDKEJKjdkjgkjKDJJKjiei439954JKJDFK9482jkgKJDKjgijiKDJ394'}

@aiohttp_jinja2.template('login.jinja2')
async def loginPage(request):
    data={}
    data['title']='登录' 
    data['main']=static.assets           
    return data
    pass

async def login(request): 
    data={}
    data['title']='Hot' 
    data['main']=static.assets
    #print(dir(request),'\n\n')
    rsp=web.Response()
    para = await request.post()
    if para['user'] == users['uid'] and para['psw'] == users['psw']:
      #res = aiohttp_jinja2.render_template('inputHotKey.jinja2',request,data) 
      
      rsp.set_cookie('Authentication','JDKEJKjdkjgkjKDJJKjiei439954JKJDFK9482jkgKJDKjgijiKDJ394')
      rsp.body=b'''
        <html> 
        <head>          
        <meta http-equiv="refresh" content="0;url=http://skysaga.vicp.io:9999/private/index.html"> 
        </head>
        </html>
    '''
      return rsp
    else:
      return web.HTTPFound('/')
    


async def middleware_factory(app, handler):
    async def middleware_handler(req):
        # if req.path == '/' or req.path.startswith('/static/')\
        #         or req.cookies.get('uid') == users['psw']:
        if req.path.startswith('/private/') and \
        req.cookies.get('Authentication') != cookies['Authentication']:            
            #print(req.cookies.get('uid'))
            return web.HTTPFound('/')
            
        else: 
            #print(req.path)
            return await handler(req)
            pass
                
    return middleware_handler