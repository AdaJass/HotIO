import asyncio
from datetime import datetime as dt
from datetime import timedelta as delta
from aiohttp import web
import staticfile as static
import aiohttp_jinja2
from pathlib import Path as p
import os
import json
import shlex, subprocess
from model import *

timenow = dt.now()
global keyword, w
keyword=''
w=1

def initialDatabase(db):
    global engine
    engine=db


@aiohttp_jinja2.template('hotgraph.jinja2')
async def hotPage(request):
    data={}
    data['title']='Hot' 
    data['main']=static.assets 
    data['main']['footerjs']=['/private/js/hotgraph.js']
    data['main']['headerjs']=[
        '/statics/chart.js/dist/Chart.min.js',
        '/static/jquery/dist/jquery.min.js',    
        '/static/bootstrap/dist/js/bootstrap.min.js'    
    ] 

    return data
    pass

@aiohttp_jinja2.template('inputHotKey.jinja2')
async def searchPage(request):
    data={}
    data['title']='Hot' 
    data['main']=static.assets           
    return data
    pass

@asyncio.coroutine
def hotData(request):  #返回数据
    # print('hotData')
    global engine, keyword, w 
    baidu=[]
    sogou=[]
    _360=[]
    # return web.Response(body='S')

    with (yield from engine) as conn:            
        objt = yield from conn.execute(obj.select().where(obj.c.main==keyword))
        objid=0
        for row in objt:
            # print(row)
            objid=row.id
            w=row.weight      
        tem=yield from conn.execute(his.select().where(his.c.objectid == objid).order_by(his.c.dtime)) 
        yield from conn.execute('commit')
        ii=0
        for row in tem:
            ii+=1            
            baidu.append(row.baidu_pages)
            sogou.append(row.sogou_pages)
            _360.append(row._360_pages)
            if ii>=73:
                break

    # print(len(sogou),'\n', sogou, end='\n up is sogou.')
    # print('-----',objid,'-----','\n', baidu, end='\n up is baidu.')

    data=[]
    for i in range(73):
        try:
            data.append(w*(0.265*baidu[i]+0.335*sogou[i]+0.4*_360[i]))
        except TypeError:
            tem=[baidu[i],sogou[i], _360[i]]
            akgd=filter(lambda x:type(x) == type(0), tem)  
            tt=0
            for i in akgd:
                tt += i
            if tt:
                data.append(w*tt)
            else:
                data.append(w)
        except IndexError:            
            break   
    res={}
    if len(data)<72:
        data=[0 for i in range(73)]
    res['data']=data
    res['title']=keyword
    res['labels']=[i*5 for i in range(73,0,-1)]
    res['labels'][72]='5天前'
    res['labels'][0]='一年前'
    res['labels'][36]='半年前'
    return web.Response(body=json.dumps(res).encode('utf-8'),content_type='application/json')


async def dynamicResultPage(request): #解析查询字符。调用Hot函数
    timenow=dt.now()   
    para = await request.post()    
    search={}    
    if para['keyword']=='':
        return web.HTTPFound('/')
    if not para.get('andDescript'):
        search['andDescript'] = '0'
    else:
        search['andDescript']=para['andDescript']
    if not para.get('orDescript'):
        search['orDescript']='0'
    else:
        search['orDescript']=para['orDescript']

    search['keyword']=para['keyword']
    global keyword
    keyword=para['keyword']
    evalStr='python ../Hot/main.py '+search['keyword']+' '\
              +search['andDescript']+' '+search['orDescript']
    evalStr = shlex.split(evalStr)
    # print(evalStr)
    subprocess.Popen(evalStr)
    print(search,end='\n this is posted data.')    
    return web.HTTPFound('/private/hotgraph')


# @aiohttp_jinja2.template('searchResult.jinja2')
# async def makeSearch(request):
#     '''
#     make the hot search engine start 
#     and the redirect to the result page
#     '''
#     para = await request.post()
#     #print(para, '  sssssss')
    
#     if para['keyword']=='':
#         return web.HTTPFound('/')

#     evalStr='start /MIN python ../Hot/main.py '+para['keyword']+' '\
#               +para['limit0']+' '+para['limit1']+' '+para['limit2']

#     if para.get('is_save')=='on':
#         evalStr+=' '+'1'
#     else:
#         evalStr+=' ' + '0'

#     os.system(evalStr)
    
#     print(evalStr)
    

#     data={}
#     data['title']='查询结果' 
#     data['main']=static.assets           
#     return data
#     pass

# async def responseResult(request):
#     text=''
#     n=0
#     for x in p('./private/pictures').iterdir():
#         if x.is_file():                        
#             if x.match('*.jpg'):                
#                 text+=x.stem+','
#                 n+=1
#     if n == 3:
#         text='1'
#     if n==0:
#         text='0'

#     return web.Response(body=text.encode('utf-8'))

# async def beautyResultPage(request): 
#     timenow=dt.now()   
#     para = await request.post()
#     #print(para, '  sssssss')
    
#     if para['keyword']=='':
#         return web.HTTPFound('/')

#     evalStr='start /MIN python ../Hot/main.py '+para['keyword']+' '\
#               +para['limit0']+' '+para['limit1']+' '+para['limit2']

#     if para.get('is_save')=='on':
#         evalStr+=' '+'1'
#     else:
#         evalStr+=' ' + '0'

#     os.system(evalStr)
#     for x in p('./private/graphData').iterdir():
#         if x.is_file():                        
#             if x.match('tieba.json') or x.match('baidu.json') or x.match('zhihu.json'):                
#                 os.remove('./'+str(x))
#     return web.HTTPFound('/private/hotgraph.html')

# D={
#     'baidu':'people',
#     'zhihu':'clicks',
#     'tieba':'conversions'
# }


# def graphData(request):
#     n=0
#     resjson=[]
#     para = request.GET
#     start=''
#     end=''
#     if para.get('start'):
#         start=para['start']
#     else:
#         start=dt.strftime(dt.now(),'%Y-%m-%d')

#     if para.get('end'):
#         end=para['end']
#     else:
#         end=dt.strftime(dt.now()-delta(days=180),'%Y-%m-%d')

#     start=dt.strptime(start,'%Y-%m-%d')
#     end=dt.strptime(end,'%Y-%m-%d')

#     if start >end:
#         start, end = end, start


#     # print(para) 
#     for x in p('./private/graphData').iterdir():
#         if x.is_file():                        
#             if x.match('tieba.json') or x.match('baidu.json') or x.match('zhihu.json'):
#                 n+=1
#                 name=str(x.stem)
#                 with open('./private/graphData/'+name+'.json', 'r') as f:
#                     js=json.loads(f.read())
#                     for key in js:
#                         thedate=dt.strptime(key,'%Y-%m-%d')
#                         if thedate>end or thedate<start:
#                             continue
#                         for index, value in enumerate(resjson):                            
#                             if value['date'] == key:
#                                 # print('##','keyis ',key,' ')
#                                 resjson[index][D[name]] = js[key]
#                                 break
#                         else:
#                             resjson.append({
#                                 'date': key,
#                                 D[name]: js[key]
#                             })

#     if n < 3 and timenow+delta(0,20,0)>dt.now():
#         return web.Response(body='no completed'.encode('utf-8'))


#     # resStr=""
#     # with open('./private/graphData/graph.json','r') as f:
#     #     resStr=f.read() 
#     if len(resjson)>0:
#         if not resjson[0].get('people'):
#             resjson[0]['people']=0
#     resjson=sorted(resjson,key=lambda t : dt.strptime(t['date'],'%Y-%m-%d'))   
#     resStr = json.dumps(resjson)
#     # print(resjson)
#     return web.Response(body=resStr.encode('utf-8'))
