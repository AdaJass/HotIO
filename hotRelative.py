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

def initialDatabase(db):
    global engine
    engine=db

def relativePara(request):

    pass

def coreRelative(data):  #it just compare two array sets relativity.

    pass