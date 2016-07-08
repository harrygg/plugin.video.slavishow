# -*- coding: utf-8 -*-
import re, sys, urllib, os.path
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from resources.lib.helper import *
reload(sys)  
sys.setdefaultencoding('utf8')

# append pydev remote debugger
REMOTE_DBG = False
if REMOTE_DBG:
	try:
		sys.path.append("C:\\Software\\Java\\eclipse-kepler\\plugins\\org.python.pydev_4.3.0.201508182223\\pysrc")
		import pydevd
		xbmc.log("After import pydevd")
		#import pysrc.pydevd as pydevd # with the addon script.module.pydevd, only use `import pydevd`
		# stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
		pydevd.settrace('localhost', stdoutToServer=False, stderrToServer=False, suspend=False)
	except ImportError:
		xbmc.log("Error: You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
		sys.exit(1)
	except:
		xbmc.log("Unexpected error:", sys.exc_info()[0]) 
		sys.exit(1)
helper = Helper()

addon = xbmcaddon.Addon(id='plugin.video.slavishow')
icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), "icon.png"))

def Categories(name = None):
	helper.Update(addon, 'browse', 'Categories')
	cats = helper.Categories(name)
	for c in cats:
		if URL in c.keys():
			AddDir(c[NAME].encode('utf-8'), c[URL].encode('utf-8'), Mode.Videos)
		else:
			AddDir(c[NAME].encode('utf-8'), "", Mode.Categories)
	
def Videos(url, page):
	videos = helper.Videos(url, page)
	for v in videos:
		AddLink(v[TITLE].encode('utf-8'), v[URL], v[ICON])
	if helper.has_more_videos:
		page = page + 1
		AddDir('Следваща страница >>>', url, Mode.Videos, page)
	
def Play(name, url, img):
	url = helper.VideoStream(url)
	xbmc.log('SlaviShow | play() | Trying to play item: ' + url)
	li = xbmcgui.ListItem(iconImage = img, thumbnailImage = img, path =  url)
	li.setInfo('video', { TITLE: name })
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

try: name = urllib.unquote_plus(params[NAME])
except: name = None

try: url = urllib.unquote_plus(params[URL])
except: url = None

try: mode = int(params["mode"])
except: mode = 1

try: page = int(params["page"])
except: page = 1

if mode == 1 or  mode == None:
	Categories(name)

elif mode == Mode.Videos:
	Videos(url, page)

elif mode == Mode.Play:
	Play(name, url, icon)

xbmcplugin.endOfDirectory(int(sys.argv[1]))