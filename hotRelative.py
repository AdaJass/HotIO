import asyncio
from datetime import datetime as dt
from datetime import timedelta as delta
from aiohttp import web
import staticfile as static
import aiohttp_jinja2
from pathlib import Path as p
import os
import json
from model import *

RelatKeys=[]
AllData=[]
def initialDatabase(db):
    global engine
    engine=db

def getRelateData():  #it return two rough array that gona to be analyse    
    for index,keyword in enumerate(RelatKeys):
        baidu=[]
        sogou=[]
        _360=[]
        data=[]
        with (yield from engine) as conn:            
            objt = yield from conn.execute(obj.select().where(obj.c.main==keyword))
            objid=0
            for row in objt:
                objid=row.id
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
        
        for i in range(73):
            try:
                data.append(0.265*baidu[i]+0.335*sogou[i]+0.4*_360[i])
            except TypeError:
                tem=[baidu[i],sogou[i], _360[i]]
                akgd=filter(lambda x:type(x) == type(0), tem)  
                tt=0
                for i in akgd:
                    tt += i
                if tt:
                    data.append(tt)
                else:
                    data.append(0)
            except IndexError:            
                break   
        if len(data)<72:
            data=[0 for i in range(73)]

        AllData.append(data.copy())
    pass

def coreRelative(s1,s2):  #it just compare two array sets relativity.
    l=len(s1)
    sum1=0
    for i in s1:
        sum1+=i
    sum2=0.0
    for i in s2:
        sum2+=i
    aver1=sum1/l
    aver2=sum2/l
    bothdiff=0.0
    squrediff1=0.0
    squrediff2=0.0
    for i in range(l):
        bothdiff+=(s1[i]-aver1)*(s2[i]-aver2)
        squrediff1+=(s1[i]-aver1)**2
        squrediff2+=(s2[i]-aver2)**2
    r=bothdiff/(squrediff1*squrediff2)**0.5 
    return r       
    pass

def controler():

    pass