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

RelatKeys=[]  #保存着所有待分析的词，第一个是中心词
AllData=[]    #保存着所有待分析词的对应数据
def initialDatabase(db):
    global engine
    engine=db

@asyncio.coroutine
def getRelateData(keyword):  #it return all rough array for each keyword that gona to be analyse    
    # for index,keyword in enumerate(RelatKeys):
    if len(RelatKeys) > len(AllData):
        baidu=[]
        sogou=[]
        _360 =[]
        data= []
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

def controler():   #shifts the arrays and make relative indicator largest and them out put
                   #all except the first one, compare to the first array.
                   #output the max correlation coefficient coresponding and its shift by each keyword.
    s1=[],s2=[],r=[]
    for i in range(1,len(AllData)):
        r.append([])
        for j in range(36):
            s1=AllData[0][j:]
            if j==0:
                s2=AllData[i]
            else:
                s2=AllData[i][0:-j]
            r[i-1].append(coreRelative(s1,s2))

    output=[]
    for arr in r:
        maxitem = max(arr)
        maxindex = arr.index(maxitem)
        output.append([maxindex,maxitem])

    return output
    pass


def compare2(keyword):   #shifts the arrays and make relative indicator largest and them out put
                          #compare the keyword relative data to the first array.
                          #output the max correlation coefficient coresponding and its shift by each keyword.
    s1=[]
    s2=[]
    r=[]
    index=RelatKeys.index(keyword)
    for j in range(36):
        s1=AllData[0][j:]
        if j==0:
            s2=AllData[index]
        else:
            s2=AllData[index][0:-j]
        r.append(coreRelative(s1,s2))

     
    maxitem = max(r)
    maxindex = r.index(maxitem)   

    return [maxindex,maxitem]
    pass