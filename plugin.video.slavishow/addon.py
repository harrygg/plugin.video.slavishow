# -*- coding: utf-8 -*-
import re, sys, urllib, os.path
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from resources.lib.helper import *
reload(sys)  
sys.setdefaultencoding('utf8')

class Mode:
    Categories = 1
    Videos = 2
    Play = 3

helper = Helper()
URL = 'url'

def Categories(name = None):
	cats = helper.Categories(name)
	for c in cats:
		if URL in c.keys():
			AddDir(c['name'].encode('utf-8'), c['url'].encode('utf-8'), Mode.Videos)
		else:
			AddDir(c['name'].encode('utf-8'), "", Mode.Categories)
	
def Videos(url, page):
	videos = helper.Videos(url, page)
	for v in videos:
		AddLink(v['title'].encode('utf-8'), v['url'], v['icon'])
	if helper.has_more_videos:
		page = page + 1
		AddDir('Следваща страница >>>', url, Mode.Videos, page)
	
def Play(name, url, img):
	url = helper.VideoStream(url)
	xbmc.log('SlaviShow | play() | Will try to play item: ' + url)
	li = xbmcgui.ListItem(iconImage = img, thumbnailImage = img, path =  url)
	li.setInfo('video', { 'title': name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path = url))

def AddLink(name, url, img):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=3&name=" + urllib.quote_plus(name)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = img, thumbnailImage = img)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty("IsPlayable" , "true")
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)
	return ok

def AddDir(name, url, mode = Mode.Categories, page = 1):
	u = sys.argv[0] + "?name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&page=" + str(page)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = icon, thumbnailImage = icon)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

params = GetParams()

name = None
try: name = urllib.unquote_plus(params["name"])
except: pass

url = None
try: url = urllib.unquote_plus(params["url"])
except: pass

_addon = xbmcaddon.Addon(id='plugin.video.slavishow')
icon = xbmc.translatePath(os.path.join(_addon.getAddonInfo('path'), "icon.png"))
try: icon = urllib.unquote_plus(params["icon"])
except: pass

mode = 1
try: mode = int(params["mode"])
except: pass

page = 1
try: page = int(params["page"])
except: pass

if mode == 1 or  mode == None:
	Categories(name)

elif mode == Mode.Videos:
	Videos(url, page)

elif mode == Mode.Play:
	Play(name, url, icon)

xbmcplugin.endOfDirectory(int(sys.argv[1]))