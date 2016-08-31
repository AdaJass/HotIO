import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
import Auth
import staticfile as static
import hot
import vote
from aiomysql.sa import create_engine
from model import *

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
    res.set_cookie('Authentication','logout')
    return res
    
@asyncio.coroutine
def Database(future):
    '''
    data is from the http response in main module.
    '''
    global engine
    engine = yield from create_engine(user='root',db='hot',port=3306,\
                                        host='127.0.0.1', password='11111',\
                                        echo=True, charset='utf8')
    future.set_result(engine)


@asyncio.coroutine
def CloseDB():
    engine.close()
    yield from engine.wait_closed()    
    pass
# web.run_app(app,port=9999)
async def init(loop):
    app = web.Application(middlewares=[Auth.middleware_factory])
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader('./view'))

    app.router.add_route('GET', '/', Auth.loginPage)
    app.router.add_route('GET', '/private/search', hot.searchPage)
    app.router.add_route('GET','/private/result_data', hot.hotData)
    app.router.add_route('GET','/private/hotgraph', hot.hotPage)

    app.router.add_route('POST', '/login', Auth.login)
    app.router.add_route('POST', '/private/makesearch', hot.dynamicResultPage)
    app.router.add_route('POST', '/succeedregist', vote.succeedregist)
    app.router.add_route('POST','/logout', logout)
    # app.router.add_route('GET','/private/respond_data', hot.graphData)
    app.router.add_static('/static/', './bower_components')
    app.router.add_static('/statics/', './node_modules')
    app.router.add_static('/private/', './private')
    app.router.add_static('/','./public')
    srv = await loop.create_server(
        app.make_handler(), '0.0.0.0', 9999)
    print('Sever starts at port: 9999')
    return srv

if __name__ == '__main__':    
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(Database(future))
    loop.run_until_complete(future)
    engine = future.result() 

    hot.initialDatabase(engine)  
    
    loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass