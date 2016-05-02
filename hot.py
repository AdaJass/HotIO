import asyncio
from datetime import datetime as dt
from aiohttp import web
import staticfile as static
import aiohttp_jinja2
from pathlib import Path as p
import os

@aiohttp_jinja2.template('inputHotKey.jinja2')
async def searchPage(request):
    data={}
    data['title']='登录' 
    data['main']=static.assets           
    return data
    pass

@aiohttp_jinja2.template('searchResult.jinja2')
async def makeSearch(request):
    '''
    make the hot search engine start 
    and the redirect to the result page
    '''
    para = await request.post()
    #print(para, '  sssssss')
    
    if para['keyword']=='':
        return web.HTTPFound('/')

    evalStr='start /MIN python ../Hot/main.py '+para['keyword']+' '\
              +para['limit0']+' '+para['limit1']+' '+para['limit2']

    if para.get('is_save')=='on':
        evalStr+=' '+'1'
    else:
        evalStr+=' ' + '0'

    # print(evalStr)
    os.system(evalStr)
    for x in p('./public/pictures').iterdir():
        if x.is_file():                        
            if x.match('*.jpg'):
                #print(x)
                os.remove('./'+str(x))

    data={}
    data['title']='登录' 
    data['main']=static.assets           
    return data
    pass

def responseResult(request):
    text=''
    n=0
    for x in p('./public/pictures').iterdir():
        if x.is_file():                        
            if x.match('*.jpg'):                
                text+=x.stem+','
                n+=1

    if n == 4:
        text='1'
    if n==0:
        text='0'
    
    return web.Response(body=text.encode('utf-8'))

