import sys, xbmc, os.path, json, urllib2, re, HTMLParser

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
            ul = re.compile('ul.+video_list["\']+>(.+?)</ul', re.DOTALL).findall(response)
            if len(ul)>0:
                m = re.compile('a.+href[="\'\s]+(.+?)["\'\s]+.+title[="\']+(.+?)[\'"]+.+img.*src[="\']+(.+?)[\'"]+').findall(ul[0]) 
                h = re.compile('a.+class[\'"=]+(next.+page-numbers)').findall(response)
                self.has_more_videos = True if len(h) > 0 else False
                h = HTMLParser.HTMLParser()
                if len(m) > 0:
                    for i in range(0, len(m)):
                        video = {}
                        video['url'] = m[i][0]
                        unescaped = h.unescape(m[i][1])
                        video['title'] = unescaped
                        video['icon'] = m[i][2]
                        videos.append(video) 
        except Exception, er:
            xbmc.log("Slavishow | ExtractVideos() " + str(er))
        return videos
 
        
    def VideoStream(self, url):
        host = 'rtmp://audio.slavishow.com/slavishow/'
        player = self.host + 'content/themes/slavishow/sw.f/flowplayer.cluster-3.2.10.swf'
        path = ''                                                            
        try:
            html = Request(url)
            h = re.compile('host["\':\s]+(rtmp.+?)["\'\s]').findall(html)
            if len(h) > 0:
                host = h[0]
            m = re.compile('url["\':\s]+(.+\.mp4)["\'\s]').findall(html)
            if len(m) > 0:
                path = m[0]
        except Exception, er:
            xbmc.log("Error in VideoStream(url = %s): " % url + str(er))
        
        stream = '%s swfUrl=%s pageUrl=%s playpath=%s' % (host, player, url, path)
        return stream
    
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