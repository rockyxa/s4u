#s4u.se/
#PYTHON VERSION IS 2.5.4
import os, zipfile

#API_URL = 'http://s4u.se/xml.php?q=%s'
API_URL = 'http://api.s4u.se/beta/DemoKey/xml/movie/imdb/%s'

def Start():
  HTTP.CacheTime = CACHE_1DAY
  
class s4uAgentMovies(Agent.Movies):
  name = 's4u'
  languages = [Locale.Language.English, Locale.Language.Swedish]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.imdb']
  
  def scoreHeuristic(self,releasename,releasepath):
    #ESTIMATE SCORE BY MATCHING RELEASENAME AND LOCAL FILENAME (DIRECTORY NAME REALLY)
    Log("Comparing %s with %s" % (releasename, releasepath))
    distance = Util.LevenshteinDistance(releasename, releasepath)
    return distance
  
  def search(self, results, media, lang):
    #SCORE IF WE HAVE AN IMDB ID
    searchScore = 0; 
    if media.primary_metadata.id is not None:
      imdbId = media.primary_metadata.id
      if imdbId.startswith('tt'):
        imdbId = imdbId[2:]
        searchScore = 100
    
    Log("Search: imdbId: %s" % imdbId)    
    Log("Search: score: %s:" % searchScore)
    
    results.Append(MetadataSearchResult(id = imdbId,score = searchScore))
    
  def update(self, metadata, media, lang):
    #NAME & PATH
    filename = media.items[0].parts[0].file.decode('utf-8')       
    path = os.path.dirname(filename)
    if 'video_ts' == path.lower().split('/')[-1]:
      path = '/'.join(path.split('/')[:-1])
    basename = os.path.basename(filename)
    releasepath = path.split("/")
    releasepath = releasepath.pop()
    
    Log("Update: filename: %s" % filename)
    Log("Update: path: %s" % path)
    Log("Update: basename: %s" % basename)
    Log("Update: releasepath: %s" % releasepath)
  	
  	#XMLURL
    xmlUrl = API_URL % metadata.id    
    Log("Update: xmlUrl: %s" % xmlUrl)
    
    #PARSE XML
    subList = []
    bestScore = 0
    bestFileToDownload = ""
    bestReleaseName = ""
    
    xmlRes = XML.ElementFromURL(xmlUrl, cacheTime=60)
    Log("Update: xmlRes: %s" % xmlRes)
    for sub in xmlRes.xpath("//sub"):
      releasename = sub.xpath("rls")[0].text
      file = sub.xpath("download_zip")[0].text
      Log("Releasename: %s" % releasename)
      Log("File: %s" % file)
      score = 100 - self.scoreHeuristic(releasename,releasepath)
      if score > bestScore:
        bestScore = score
        bestReleaseName = releasename
        bestFileToDownload = file
      Log("Score: %s" % score)
      
    Log("Result-------------------")
    Log("Best score: %s" % bestScore)
    Log("Releasename: %s" % bestReleaseName)
    Log("File to download: %s" % bestFileToDownload)
    
    #Log("Zip-tester")
    #file = zipfile.ZipFile("samples/sample.zip", "r")

    # list filenames
    #for name in file.namelist():
      #print name,
    #print
	
	#DOWNLOAD FILE
    if bestScore > 85: #JUSTERA DETTA SEN
      try:
        #subFile = HTTP.Request(bestFileToDownload, headers={'Accept-Encoding':''}).content
        #myfile = open("/Users/Johan/Downloads/ziptest/testit.txt", "wb")
        #Log('Update: Downloading sub from %s' % bestFileToDownload)
        #Log('Update: Downloaded file %s' % myfile)
        pass        
      except:
        #Log('Update: Failed to download sub from %s' % bestFileToDownload)      
        pass
      try:
        #subData = Archive.GzipDecompress(subFile)
        pass
      except:
        #Log('Update: Misslyckades med uppackning')
        pass
          
      for i in media.items:
        for p in i.parts:
          pass
          #try:
            #p.subtitles[Locale.Language.Swedish][subUrl] = Proxy.Media(subData, ext="srt")
          #except:
            #Log('Update: Misslyckades att uppdatera')