#!/usr/bin/env python3

from urllib.request import urlopen, urlretrieve
from shutil import copyfileobj
from datetime import datetime
import json

timeformat = '%Y-%m-%dT%H:%M:%S.%f'
lastfile = 'update/last'

def parsetime(timestring:str):
  return datetime.strptime(timestring, timeformat)

def readlast():
  with open(lastfile, 'r') as f:
    return parsetime(f.read())

def writelast(timestring:str):
  with open(lastfile, 'w+') as f:
    f.write(timestring.strftime(timeformat))
  
def savefile(fileurl:str):
  filename = fileurl.split('/')[-1]
  urlretrieve(fileurl, 'datos/' + filename)
  return filename
  
def update(dataset:str):
  updated = []
  last = now = readlast()
  url = 'https://datos.gob.bo/api/3/action/package_show?id={}'
  response = json.loads(urlopen(url.format(dataset)).read())
  for resource in response['result']['resources']:
    last_modified = parsetime(resource['last_modified'])
    if last_modified > last:
      updated.append(savefile(resource['url']))
      if last_modified > now:
        now = last_modified
  if now != last:
    writelast(now)
    print(', '.join(updated))
  else:
    print('nada')

update('casos-covid-19-acumulado-por-municipios')
