# -*- coding: utf-8 -*-
import sys, xbmc, os.path, json, urllib2, re, HTMLParser
from ga import ga
from bs4 import BeautifulSoup

class Helper():
  has_more_videos = False
  host = 'http://www.slavishow.com/'
  
  def SubCats(self, name, data):
    for c in data['categories']:
      n = c['name']
      if n == name:
        return c["categories"]
              
  def Categories(self, name = ''):
    cats = []
    try:
      filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'categories.json')
      with open(filename) as data_file:
        data = json.load(data_file)
      
      if name == None:
        cats = data["categories"]
      else:
        cats = self.SubCats(name, data)
    except Exception, er:
      xbmc.log("SlavShow | get_categories() | Error: " + str(er))
            
    return cats
  
  def Videos(self, url, page):
    if page > 1: 
      url = url + 'page/' + str(page)
    res = Request(self.GetUrl(url))
    v = self.ExtractVideos(res)
    return v
  
  def GetUrl(self, url):
    return self.host + url
  
  def ExtractVideos(self, response):
    videos = []
    try:
      soup = BeautifulSoup(response.decode('utf-8', 'ignore'), 'html5lib')
      ul = soup.find('ul', class_='video_list')
      if ul != None:
        self.has_more_videos = True if soup.find('a', class_='next page-numbers') else False
        imgs = ul.find_all('img')
        h3s = ul.find_all('h3')

        for i in range(0, len(imgs)):
          v = {}
          v['url'] = h3s[i].a['href']
          v['title'] = h3s[i].a.get_text()
          v['icon'] = imgs[i]['src']
          videos.append(v)
      else:
      	xbmc.log(response)
    except Exception, er:
        xbmc.log("Slavishow | ExtractVideos() " + str(er))
    return videos
  
      
  def VideoStream(self, url):
    host = 'rtmp://audio.slavishow.com/slavishow/'
    player = 'http://vjs.zencdn.net/swf/5.0.1/video-js.swf'
    path = ''                                                            
    try:
      html = Request(url)
      h = re.compile('host["\':\s]+(rtmp.+?)["\'\s]').findall(html)
      if len(h) > 0:
        host = h[0]
      m = re.compile('input.*value.*["\'\s]+(.+\.mp4)["\'\s]').findall(html)#<input type="hidden" id="wm-src-video" value="slavishow/20160201.mp4">
      if len(m) > 0:
        path = m[0]
    except Exception, er:
      xbmc.log("Error in VideoStream(url = %s): " % url + str(er))
    
    stream = '%s swfUrl=%s pageUrl=%s playpath=%s' % (host, player, url, path)
    return stream
     
  def Update(self, addon, name, location, crash=None):
    p = {}
    p['an'] = addon.getAddonInfo('name')
    p['av'] = addon.getAddonInfo('version')
    p['ec'] = 'Addon actions'
    p['ea'] = name
    p['ev'] = '1'
    p['ul'] = xbmc.getLanguage()
    p['cd'] = location
    ga('UA-79422131-5').update(p, crash)
        
def Request(url, data = ''):
  xbmc.log("Slavishow | Sending request to: " + url)
  try:
    req = urllib2.Request(url) if data == '' else urllib2.Request(url, data) 
    res = urllib2.urlopen(req)
    response = res.read()
    res.close()
    return response
  except Exception, er:
    xbmc.log("Slavishow | Request error: " + str(er))
    return ""

def GetParams():
  param=[]
  paramstring=sys.argv[2]
  if len(paramstring)>=2:
    params=sys.argv[2]
    cleanedparams=params.replace('?','')
    if (params[len(params)-1]=='/'):
      params=params[0:len(params)-2]
    pairsofparams=cleanedparams.split('&')
    param={}
    for i in range(len(pairsofparams)):
      splitparams={}
      splitparams=pairsofparams[i].split('=')
      if (len(splitparams))==2:
        param[splitparams[0]]=splitparams[1]
  return param
 
URL = 'url'
ICON = 'icon'
NAME = 'name'
TITLE = 'title'


class Mode:
  Categories = 1
  Videos = 2
  Play = 3