import asyncio
from datetime import datetime as dt
from datetime import timedelta as delta
from aiohttp import web
import staticfile as static
import aiohttp_jinja2
from pathlib import Path as p
import os
import json

@aiohttp_jinja2.template('inputHotKey.jinja2')
async def searchPage(request):
    data={}
    data['title']='Hot' 
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

    os.system(evalStr)
    
    print(evalStr)
    

    data={}
    data['title']='查询结果' 
    data['main']=static.assets           
    return data
    pass

async def responseResult(request):
    text=''
    n=0
    for x in p('./private/pictures').iterdir():
        if x.is_file():                        
            if x.match('*.jpg'):                
                text+=x.stem+','
                n+=1

    if n == 3:
        text='1'
    if n==0:
        text='0'
    
    return web.Response(body=text.encode('utf-8'))

async def beautyResultPage(request):    
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

    os.system(evalStr)
    for x in p('./private/graphData').iterdir():
        if x.is_file():                        
            if x.match('tieba.json') or x.match('baidu.json') or x.match('zhihu.json'):                
                os.remove('./'+str(x))
    return web.HTTPFound('/private/hotgraph.html')

D={
    'baidu':'people',
    'zhihu':'clicks',
    'tieba':'conversions'
}

def graphData(request):
    n=0
    resjson=[]
    para = request.GET
    start=''
    end=''
    if para.get('start'):
        start=para['start']
    else:
        start=dt.strftime(dt.now(),'%Y-%m-%d')

    if para.get('end'):
        end=para['end']
    else:
        end=dt.strftime(dt.now()-delta(days=180),'%Y-%m-%d')

    start=dt.strptime(start,'%Y-%m-%d')
    end=dt.strptime(end,'%Y-%m-%d')

    if start >end:
        start, end = end, start


    # print(para) 
    for x in p('./private/graphData').iterdir():
        if x.is_file():                        
            if x.match('tieba.json') or x.match('baidu.json') or x.match('zhihu.json'):
                n+=1
                name=str(x.stem)
                with open('./private/graphData/'+name+'.json', 'r') as f:
                    js=json.loads(f.read())
                    for key in js:
                        thedate=dt.strptime(key,'%Y-%m-%d')
                        if thedate>end or thedate<start:
                            continue
                        for index, value in enumerate(resjson):                            
                            if value['date'] == key:
                                # print('##','keyis ',key,' ')
                                resjson[index][D[name]] = js[key]
                                break
                        else:
                            resjson.append({
                                'date': key,
                                D[name]: js[key]
                            })

    # if n >= 3:
    #     return web.Response(body='OK'.encode('utf-8'))


    # resStr=""
    # with open('./private/graphData/graph.json','r') as f:
    #     resStr=f.read() 
    resjson=sorted(resjson,key=lambda t : dt.strptime(t['date'],'%Y-%m-%d'))   
    resStr = json.dumps(resjson)
    # print(resjson)
    return web.Response(body=resStr.encode('utf-8'))
