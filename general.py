from datetime import date,timedelta, datetime
from classes import *
import requests
import xmltodict
"""
General Functions
"""
def get_matches(arguments,files):
    torrentfolder=arguments['--torrent']
    api=arguments['--api']
    cookie=arguments['--cookie']
    datefilter=(date.today()- timedelta(int(arguments['--date'])))
    file=files.get_first()
    if file=="No Files":
        return
    filesize=files.get_size()
    fileguessit=guessitinfo(file)
    fileguessit.set_values()
    title=fileguessit.get_name().lower()
    if fileguessit.get_season()!="":
        title=title+": " + fileguessit.get_season()
    imdb=get_imdb(fileguessit.get_info())
    if imdb==None:
        print(file," could not be parsed")
        return
    search = "https://awesome-hd.me/searchapi.php?action=imdbsearch&passkey=" + api + "&imdb=tt" + imdb
    print("Searching For",files.type,"with:",search)
    try:
        response = requests.get(search, timeout=120)
    except:
        print("Issue getting response:",search)
        return
    results=xmltodict.parse(response.content)
    try:
        results['searchresults']['torrent'][1]['name']
        loop=True
        max=len(results['searchresults']['torrent'])
    except KeyError as key:
        if str(key)=="1":
            element=results['searchresults']['torrent']
            max=1
            loop=False
        else:
            print("Probably no results")
            return
    for i in range(max):
        title=False
        filedate=False
        group=False
        resolution=False
        source=False
        sizematch=False
        if loop: element = results['searchresults']['torrent'][i]
        querytitle=lower(element['name'])
        if querytitle==None:
            continue
        querygroup=lower(element['releasegroup'])
        queryresolution=element['resolution']
        querysource=lower(element['media'])
        if querysource=="uhd blu-ray":
            querysource="blu-ray"
        queryencoding=element['encoding']
        querysize= int(element['size'])
        querydate=datetime.strptime(element['time'], '%Y-%m-%d %H:%M:%S').date()
        if querytitle==fileguessit.get_name():
            title=True
        if querysource==fileguessit.get_source():
            source=True
        if querygroup==fileguessit.get_group():
            group=True
        if queryresolution==fileguessit.get_resolution():
            resolution==True
        if datefilter < querydate:
            filedate=True
        if difference(querysize,filesize)<.01:
            sizematch=True
        if (title is True and source is True and group is True and resolution is True \
        and filedate is True) or ((filedate is True and group is True and sizematch is True) and filesize!=0):
            pass
        else:
            continue
        if arguments['--output']!=None  and arguments['--output']!="" and arguments['--output']!="None":
            link="https://awesome-hd.me/torrents.php?id=" + element['groupid']+"&torrentid="+ element['id']
            t=open(arguments['--output'],'a')
            print("writing to file:",arguments['--output'])
            t.write(link+'\n')
        if arguments['--torrent']!=None and arguments['--torrent']!="" and  arguments['--torrent']!="None":
            link="https://awesome-hd.me/torrents.php?action=download&id=" +element['id'] +"&torrent_pass=" +  api
            name=(element['name']+ "." + element['year']+ "." + element['media']+ "." + element['resolution']+ "." + element['encoding']). replace(" ",".")
            torrent=torrentfolder + ("[ahd]"+ name +".torrent").replace("/", "_")
            print(torrent,'\n',link)
            try:
                subprocess.run(['wget','--load-cookies',cookie,link,'-O',torrent])
            except:
                print("web error")
def get_imdb(details):
   title = details.get('title')
   ia = IMDb()
   if title==None:
       return title
   for i in range(0,16):
       if i==15:
           return None
       try:
         results = ia.search_movie(title)
         break
       except Exception as e:
           time.sleep(10)
   if len(results) == 0:
        return None
   if 'year' in details:
    for movie in results:
        if ((details.get('year')==movie.get('year')) and (movie.get('year')!=None or details.get('year')!=None )):
            return movie.movieID
    return None
   else:
      return results[0].movieID
def difference(value1,value2):
    dif=abs((value2-value1)/((value1+value2)/2))
    return dif
def lower(input):
    if input==None:
        return input
    else:
        input=input.lower()
        return input
