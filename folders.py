import re
from guessit import guessit
import os
from general import *
import tempfile
import subprocess
class Folder:
    """
    Finds for example the 2160p Remux Files in a folder. Holds information about those files.
    """
    def __init__(self,dir,type,arguments):
        pass
        self.size=0
        self.type=type
        self.files=""
        self.dir=dir.strip()
        self.arguments=arguments
        self.date=datetime.now().strftime("%m.%d.%Y")
    def get_dir(self):
        return self.dir
    def get_type(self):
        return  self.type
    def get_files(self):
        return  self.files
    def get_size(self):
        return  self.size
    def get_arg(self):
        return  self.arguments
    def set_size(self):
        #error out if no files found
        temp=0
        if self.arguments["--size"]==False or self.arguments["--size"]=="F" or self.arguments["--size"]=="false" or self.arguments["--size"]=="f" or self.get_files()==None:
            self.size=temp
            return
        self.get_files().seek(0, 0)
        if len(self.get_files().readlines())<1:
            return
        self.get_files().seek(0, 0)
        for line in self.get_files().readlines():
            path=self.get_dir()+'/'+line.rstrip()
            temp=temp+os.path.getsize(path)
        self.size=temp
    def set_files(self,files):
        fd=self.arguments['--fd']
        dir=self.get_dir().rstrip()
        attempts=0
        while attempts<100:
            try:
                os.chdir(dir)
                break
            except:
                attempts=attempts+1
                print("Getting Files for:",dir,"attempt number ",attempts)
                continue
        if attempts==100:
            errorpath=pathlib.Path(__file__).parent.absolute().as_posix()+"/Errors/"
            if os.path.isdir(errorpath)==False:
                os.mkdir(errorpath)
            errorfile=errorpath+"ahdcs.errors"+self.date+".txt"
            errorfile=open(errorfile,"a+")
            errorstring="No " +self.get_type() + " Files Found: "+dir + " - " +datetime.now().strftime("%m.%d.%Y_%H%M") + "\n"
            errorfile.write(errorstring)
            errorfile.close()
            print("Unable to get Files From Directory")
            self.files = None
            return
        if self.get_type()=="remux2160":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','remux','--exclude','*1080*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="remux1080":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','remux','--exclude','*2160*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="remux720":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','remux','--exclude','*1080*',
            '--exclude','*2160*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="blu2160":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','.blu','--exclude','*1080*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[rR][eE][mM][uU][xX]*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="blu1080":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','.blu','--exclude','*2160*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[rR][eE][mM][uU][xX]*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="blu720":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','.blu','--exclude','*1080*',
            '--exclude','*2160*','--exclude','*480*','--exclude','*[rR][eE][mM][uU][xX]*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="webr2160":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','(.webr|.web-r)','--exclude','*1080*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="webr1080":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','(.webr|.web-r)','--exclude','*2160*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="webr720":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','(.webr|.web-r)','--exclude','*2160*',
            '--exclude','*1080*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="webr480":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','(.webr|.web-r)','--exclude','*2160*',
            '--exclude','*1080*','--exclude','*720*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="webdl2160":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','(.web-dl|.webdl)','--exclude','*1080*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="webdl1080":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','(.web-dl|.webdl)','--exclude','*2160*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="webdl720":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','(.web-dl|.webdl)','--exclude','*2160*',
            '--exclude','*1080*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="webdl480":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','(.web-dl|.webdl)','--exclude','*2160*',
            '--exclude','*1080*','--exclude','*720*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
        '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="web2160":
            temp=subprocess.check_output([fd,'-d','1','--glob','-e','.mkv','-e','.mp4','-e','.m4v','*.[wW][eE][bB].*','--exclude','*1080*',
            '--exclude','*720*','--exclude','*480*','--exclude','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="web1080":
            temp=subprocess.check_output([fd,'-d','1','--glob','-e','.mkv','-e','.mp4','-e','.m4v','*.[wW][eE][bB].*','--exclude','*2160*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="web720":
            temp=subprocess.check_output([fd,'-d','1','--glob','-e','.mkv','-e','.mp4','-e','.m4v','*.[wW][eE][bB].*','--exclude','*2160*',
            '--exclude','*1080*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="web480":
            temp=subprocess.check_output([fd,'-d','1','--glob','-e','.mkv','-e','.mp4','-e','.m4v','*.[wW][eE][bB].*','--exclude','*2160*',
            '--exclude','*1080*','--exclude','*720*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="tv2160":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','hdtv','--exclude','*1080*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="tv1080":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','hdtv','--exclude','*2160*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="tv720":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','hdtv','--exclude','*1080*',
            '--exclude','*2160*','--exclude','*480*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="tv480":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','hdtv','--exclude','*1080*',
            '--exclude','*2160*','--exclude','*720*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude','*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="other2160":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','--exclude','*1080*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[rR][eE][mM][uU][xX]*','--exclude','*.[wW][eE][bB]*','--exclude','*.[bB][lL][uU]*','--exclude','*[tT][vV]*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
            '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="other1080":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','--exclude','*2160*',
            '--exclude','*720*','--exclude','*480*','--exclude','*[rR][eE][mM][uU][xX]*','--exclude','*.[wW][eE][bB]*','--exclude','*.[bB][lL][uU]*','--exclude','*[tT][vV]*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
            '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="other720":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','--exclude','*1080*',
            '--exclude','*2160*','--exclude','*480*','--exclude','*[rR][eE][mM][uU][xX]*','--exclude','*.[wW][eE][bB]*','--exclude','*.[bB][lL][uU]*','--exclude','*[tT][vV]*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
            '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        elif self.get_type()=="other480":
            temp=subprocess.check_output([fd,'-d','1','-e','.mkv','-e','.mp4','-e','.m4v','--exclude','*1080*',
            '--exclude','*2160*','--exclude','*720*','--exclude','480','--exclude','*[rR][eE][mM][uU][xX]*','--exclude','*.[wW][eE][bB]*','--exclude','*.[bB][lL][uU]*','--exclude','*[tT][vV]*','--exclude','*[sS][aA][mM][pP][lL][eE]*','--exclude',
            '*[tT][rR][aA][iL][eE][rR]*']).decode('utf-8')
        files.write(temp.rstrip())
        self.files=files
    def get_first(self):
        files=self.get_files()
        try:
            files.seek(0, 0)
            first=files.readlines()[0]
            return first
        except:
            return "No Files"
    """
    Missing files Functions
    """
def scan_folder(arguments,txt,line,source):
    folders=open(txt,"r")
    if source['remux']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        remux1=Folder(line,"remux1080",arguments)
        remux1.set_files(files)
        get_missing(arguments,remux1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        remux2=Folder(line,"remux2160",arguments)
        remux2.set_files(files)
        get_missing(arguments,remux2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        remux3=Folder(line,"remux720",arguments)
        get_missing(arguments,remux3)
        files.close()
    if source['blu']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        blu1=Folder(line,"blu1080",arguments)
        blu1.set_files(files)
        get_missing(arguments,blu1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        blu2=Folder(line,"blu2160",arguments)
        blu2.set_files(files)
        get_missing(arguments,blu2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        blu3=Folder(line,"blu720",arguments)
        blu3.set_files(files)
        get_missing(arguments,blu3)
        files.close()
    if source['tv']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        tv1=Folder(line,"tv1080",arguments)
        tv1.set_files(files)
        get_missing(arguments,tv1,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        tv2=Folder(line,"tv2160",arguments)
        tv2.set_files(files)
        get_missing(arguments,tv2,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        tv3=Folder(line,"tv720",arguments)
        tv3.set_files(files)
        get_missing(arguments,tv3,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        tv4=Folder(line,"tv480",arguments)
        tv4.set_files(files)
        get_missing(arguments,tv4,True)
        files.close()
    if source['other']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        other1=Folder(line,"other1080",arguments)
        other1.set_files(files)
        get_missing(arguments,other1,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        other2=Folder(line,"other2160",arguments)
        other2.set_files(files)
        get_missing(arguments,other2,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        other3=Folder(line,"other720",arguments)
        other3.set_files(files)
        get_missing(arguments,other3,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        other4=Folder(line,"other480",arguments)
        other4.set_files(files)
        get_missing(arguments,other4,True)
        files.close()
    if source['web']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        web1=Folder(line,"web1080",arguments)
        web1.set_files(files)
        get_missing(arguments,web1,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        web2=Folder(line,"web2160",arguments)
        web2.set_files(files)
        get_missing(arguments,web2,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        web3=Folder(line,"web720",arguments)
        web3.set_files(files)
        get_missing(arguments,web3,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        web4=Folder(line,"web480",arguments)
        web4.set_files(files)
        get_missing(arguments,web4,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webr1=Folder(line,"webr1080",arguments)
        webr1.set_files(files)
        get_missing(arguments,webr1,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webr2=Folder(line,"webr2160",arguments)
        webr2.set_files(files)
        get_missing(arguments,webr2,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webr3=Folder(line,"webr720",arguments)
        webr3.set_files(files)
        get_missing(arguments,webr3,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webr4=Folder(line,"webr480",arguments)
        webr4.set_files(files)
        get_missing(arguments,webr4,True)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webdl1=Folder(line,"webdl1080",arguments)
        webdl1.set_files(files)
        get_missing(arguments,webdl1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webdl2=Folder(line,"webdl2160",arguments)
        webdl2.set_files(files)
        webdl2.set_size()
        get_missing(arguments,webdl2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webdl3=Folder(line,"webdl720",arguments)
        webdl3.set_files(files)
        webdl3.set_size()
        get_missing(arguments,webdl3)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webdl4=Folder(line,"webdl480",arguments)
        webdl4.set_files(files)
        webdl4.set_size()
        get_missing(arguments,webdl4)
        files.close()
    print("Waiting 5 Seconds")
    time.sleep(5)
###
def get_missing(arguments,files,encode=None):
    if encode==None:
        encode=False
    api=arguments['--api']
    output=arguments['--output2']
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
            print("Adding Potential Upload to File")
            output=open(output,"a+")
            output.write(files.get_dir())
            output.write(":")
            output.write(file)
            output.write('\n')
            output.close()
            return
    for i in range(max):
        title=False
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
        if querytitle==title:
            title=True
        if querysource==fileguessit.get_source():
            source=True
        if querygroup==fileguessit.get_group():
            group=True
        if queryresolution==fileguessit.get_resolution():
            resolution=True
        if difference(querysize,filesize)<.01:
            sizematch=True
        if (title is True and source is True and group is True and resolution is True \
        ) or ((group is True and sizematch is True) and filesize!=0):
            return
        if (encode==False and title is True and source is True  and resolution is True):
            return
    print("Adding Potential Upload to File")
    output=open(output,"a+")
    output.write(files.get_dir())
    output.write(":")
    output.write(file)
    output.write('\n')
    output.close()
    """
Cross Seed Torrent or Output Functions
"""
def download_folder(arguments,txt,line,source):
    folders=open(txt,"r")
    if source['remux']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        remux1=Folder(line,"remux1080",arguments)
        remux1.set_files(files)
        remux1.set_size()
        get_matches(arguments,remux1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        remux2=Folder(line,"remux2160",arguments)
        remux2.set_files(files)
        remux2.set_size()
        get_matches(arguments,remux2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        remux3=Folder(line,"remux720",arguments)
        remux3.set_files(files)
        remux3.set_size()
        get_matches(arguments,remux3)
        files.close()
    if source['blu']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        blu1=Folder(line,"blu1080",arguments)
        blu1.set_files(files)
        blu1.set_size()
        get_matches(arguments,blu1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        blu2=Folder(line,"blu2160",arguments)
        blu2.set_files(files)
        blu2.set_size()
        get_matches(arguments,blu2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        blu3=Folder(line,"blu720",arguments)
        blu3.set_files(files)
        blu3.set_size()
        get_matches(arguments,blu3)
        files.close()
    if source['tv']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        tv1=Folder(line,"tv1080",arguments)
        tv1.set_files(files)
        tv1.set_size()
        get_matches(arguments,tv1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        tv2=Folder(line,"tv2160",arguments)
        tv2.set_files(files)
        tv2.set_size()
        get_matches(arguments,tv2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        tv3=Folder(line,"tv720",arguments)
        tv3.set_files(files)
        tv3.set_size()
        get_matches(arguments,tv3)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        tv4=Folder(line,"tv480",arguments)
        tv4.set_files(files)
        tv4.set_size()
        get_matches(arguments,tv4)
        files.close()
    if source['other']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        other1=Folder(line,"other1080",arguments)
        other1.set_files(files)
        other1.set_size()
        get_matches(arguments,other1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        other2=Folder(line,"other2160",arguments)
        other2.set_files(files)
        other2.set_size()
        get_matches(arguments,other2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        other3=Folder(line,"other720",arguments)
        other3.set_files(files)
        other3.set_size()
        get_matches(arguments,other3)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        other4=Folder(line,"other480",arguments)
        other4.set_files(files)
        other4.set_size()
        get_matches(arguments,other4)
        files.close()
    if source['web']=='yes':
        files=tempfile.NamedTemporaryFile('w+')
        web1=Folder(line,"web1080",arguments)
        web1.set_files(files)
        web1.set_size()
        get_matches(arguments,web1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        web2=Folder(line,"web2160",arguments)
        web2.set_files(files)
        web2.set_size()
        get_matches(arguments,web2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        web3=Folder(line,"web720",arguments)
        web3.set_files(files)
        web3.set_size()
        get_matches(arguments,web3)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        web4=Folder(line,"web480",arguments)
        web4.set_files(files)
        web4.set_size()
        get_matches(arguments,web4)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webr1=Folder(line,"webr1080",arguments)
        webr1.set_files(files)
        webr1.set_size()
        get_matches(arguments,webr1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webr2=Folder(line,"webr2160",arguments)
        webr2.set_files(files)
        webr2.set_size()
        get_matches(arguments,webr2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webr3=Folder(line,"webr720",arguments)
        webr3.set_files(files)
        webr3.set_size()
        get_matches(arguments,webr3)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webr4=Folder(line,"webr480",arguments)
        webr4.set_files(files)
        webr4.set_size()
        get_matches(arguments,webr4)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webdl1=Folder(line,"webdl1080",arguments)
        webdl1.set_files(files)
        webdl1.set_size()
        get_matches(arguments,webdl1)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webdl2=Folder(line,"webdl2160",arguments)
        webdl2.set_files(files)
        webdl2.set_size()
        get_matches(arguments,webdl2)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webdl3=Folder(line,"webdl720",arguments)
        webdl3.set_files(files)
        webdl3.set_size()
        get_matches(arguments,webdl3)
        files.close()
        files=tempfile.NamedTemporaryFile('w+')
        webdl4=Folder(line,"webdl480",arguments)
        webdl4.set_files(files)
        webdl4.set_size()
        get_matches(arguments,webdl4)
        files.close()
