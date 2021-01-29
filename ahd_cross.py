#! /usr/bin/env python3
"""NOTE: READ DOCUMENTATION BEFORE USAGE.
Usage:
    ahd_cross.py [(-h | --help) --txt=<txtlocation> --fd <fd> --wget <wget> --config <config> --delete --lines-skip <num_lines_skipped --fdignore <fd_ignore> --log <log>]
    [--torrent <torrents_download> --cookie <cookie> --output <output> --api <apikey> --date <int>  --misstxt <output>]
    [--root <normal_root>... --ignore <sub_folders_to_ignore>...  --exclude <source_excluded>...]
    ahd_cross.py interactive [--txt=<txtlocation> --fd <fd> --wget <wget>  --config <config> --delete --lines-skip <num_lines_skipped --fdignore <fd_ignore> --log <log>]
    [--torrent <torrents_download> --cookie <cookie> --output <output> --api <apikey> --date <int> --misstxt <output>]
    [--root <normal_root>...  --ignore <sub_folders_to_ignore>...  --exclude <source_excluded>...]
    ahd_cross.py scan [--txt=<txtlocation> --fd <fd> --wget <wget> --fdignore <fd_ignore> --config <config> --delete --log <log>]
    [--root <normal_root>... --ignore <sub_folders_to_ignore>...]
    ahd_cross.py grab [--txt=<txtlocation> --fd <fd> --wget <wget> --fdignore <fd_ignore>  --lines-skip <num_lines_skipped> --torrent <torrents_download> --cookie <cookie> --output <output> --log <log> ]
    [--api <apikey> --config <config> --date <int> ]
    [--exclude <source_excluded>]...
    ahd_cross.py missing [--txt=<txtlocation> --fd <fd> --wget <wget>  --misstxt <output>  --api <apikey> --config <config> --log <log> --lines-skip <num_lines_skipped>]
    [--exclude <source_excluded>...]

Options:
 --help; -h     Show this screen.
 --txt <txtlocation>  txt file with all the file names(required for all commands)
 --api ; -a <apikey> This is your ahd passkey. Required for scanning and finding uploads
 --fd <binary_fd> fd is a program to scan for files, use this if you don't have fd in path
 --config ; -x <config> commandline overwrites config
 --fdignore <gitignore_style_ignorefile> fd .fdignore file used by fd tto find which folders to ignore, on linux it defaults to the home directory.
 other OS may need to input this manually
 --wget <wget> used to download files
 --cookie ; -c <cookie> This is a cookie file for ahd, their are numerous extensions to grab this. Required for scanning and finding uploads.
 --log ; -<logs> log file

=============================================================================================================================================

 ahd_cross.py scan
 scan tv or movie folders root folder(s) create a list of directories. 'txt file creator'. Need at least 1 root.
<required>
--root <normal_root(s)> Scan this directory. Much like the ls(linux) or dir(windows) command
<optional>
--delete; -d  Will delete the old txt file
--ignore ; -i <sub_folders_to_ignore>  folder will be ignored for scan

=============================================================================================================================================

 ahd_cross.py grab
 grab downloads torrents using txt file option to download torrent with --cookie and/or output to file.
<choose 1>
  --torrent ; -t <torrents_download>  Here are where the torrent files will download
  --output ; -o <output>  Here are where the torrentlinks will be written
<optional>
  --date ; -d <int> only download torrents newer then this input should be int, and represents days. By default it is set to around 25 years  [default: 10000 ]
  --lines-skip <num_lines_skipped> Number of lines in txt file to skip during grab  [default: 0]
  --exclude ; -e <source_excluded>  These file type(s) will not be scanned blu,tv,remux,other,web.

=============================================================================================================================================


ahd_cross.py missing
Checks to see if you have any potential uploads by comparing your files to what has already been uploaded

<required>
--misstxt <txt_where_potential_uploads_are written> here we output to a txt file files that don't have any uploads. This means that we can potentially upload these, for rank. Or to increase the amount of cross seeds we have








  """
import requests
import subprocess
import pathlib
from subprocess import PIPE
from pathlib import Path
import os
from guessit import guessit
from datetime import date,timedelta, datetime
from docopt import docopt
import tempfile
import time
import configparser
import re
config = configparser.ConfigParser(allow_no_value=True)
#import other files
from folders import *
from classes import *
from files import *
from prompt_toolkit.shortcuts import button_dialog
import sys
from shutil import which
import logging
import copy
"""
Setup Function
"""
def duperemove(txt):
    print("Removing Duplicate lines from ",txt)
    if txt==None:
        return
    input=open(txt,"r")
    lines_seen = set()
    symbols=set()
     # holds lines already seen
    i=0
    for line in input:
        start=re.search("[a-z]|[0-9]|/",line, re.IGNORECASE)
        if start==None:
            continue
        start=start.start()
        start=int(start)
        line=line[start:-1]
        if start!=0:
            symbols.add(i)
        if  line not in lines_seen:
            # not a duplicate
            lines_seen.add(line)
        i=i+1







    input.close()
    outfile = open(txt, "w")
    lines_seen=sorted(lines_seen)
    i=0
    for line in lines_seen:
        if  i in symbols:
            line="*"+line
        line=line+"\n"
        outfile.write(line)
        i=i+1
    outfile.close()
def updateargs(arguments):
    configpath=arguments.get('--config')
    if os.path.isfile(configpath)==False:
        print("Could Not Read Config Path")
        return arguments
    try:
        configpath=arguments.get('--config')
        config.read(configpath)
    except:
        print("Could Not Read Config Path")
        return arguments
    if arguments['--txt']==None:
        arguments['--txt']=config['general']['txt']
    if arguments['--cookie']==None:
        arguments['--cookie']=config['grab']['cookie']
    if arguments['--api']==None:
        arguments['--api']=config['grab']['api']
    if arguments['--torrent']==None:
        arguments['--torrent']=config['grab']['torrent']
    if arguments['--output']==None:
        arguments['--output']=config['grab']['output']
    if arguments['--misstxt']==None:
        arguments['--misstxt']=config['general']['misstxt']
    if arguments['--exclude']==[] or  arguments['--exclude']==None:
        arguments['--exclude']=config['grab']['exclude']
    if arguments['--root']==[] or  arguments['--root']==None:
        arguments['--root']=config['scan']['root']
    if arguments['--ignore']==[] or arguments['--ignore']==None:
        arguments['--ignore']=config['scan']['ignore']
    if arguments['--log']==None and len(config['general']['log'])!=0:
            arguments['--log']=config['general']['log']
    if arguments['--log']==None and len(config['general']['log'])==0:
            arguments['--log']="INFO"

    if arguments['--log'].upper() == "DEBUG":
        ahdlogger.setLevel(logging.DEBUG)
    elif arguments['--log'].upper() == "INFO":
        ahdlogger.setLevel(logging.INFO)
    else:
        ahdlogger.setLevel(logging.WARN)
    ahdlogger.debug(copy.deepcopy(arguments))

    return arguments
def releasetype(arguments):
    source={'remux':'yes','web':'yes','blu':'yes','tv':'yes','other':'yes'}
    if arguments['--exclude']==None or arguments['--exclude']==[] or arguments['--exclude']=="" or len(arguments['--exclude'])==0:
        return source
    if type(arguments['--exclude'])==str:
        arguments['--exclude']=arguments['--exclude'].split(",")
    for element in arguments['--exclude']:
        if element=="":
            continue
        try:
            source[element]="no"
        except KeyError:
            pass
    ahdlogger.debug(source)
    return source
def download(arguments):
    index=0
    txt=arguments['--txt']
    list=open(txt,"r")
    source=releasetype(arguments)
    for line in list:
        index=index+1
        ahdlogger.warn(f"Directory or File: {line}\n")
        if index<=int(arguments["--lines-skip"]):
            ahdlogger.warn(f"skipping line")
            continue
        if line=='\n' or line=="" or len(line)==0:
            continue
        line=line.rstrip("\n")

        if os.path.isdir(line)==True:
            download_folder(arguments,line,source)
        elif os.path.isfile(line)==True:
            download_file(arguments,line,source)

        else:
            currentdate=datetime.now().strftime("%m.%d.%Y_%H%M")
            ahdlogger.warn(f"{line} File or Directory Not found-{currentdate}")
            continue
        print("Waiting 5 Seconds")
        # time.sleep(5)
def missing(arguments):
    if arguments['--misstxt']=='' or len(arguments['--misstxt'])==0 or arguments['--misstxt']==None:
        ahdlogger.warn(f"misstxt must be configured for missing scan ")
        quit()
    source=releasetype(arguments)
    list=open(arguments['--txt'],"r")
    index=0
    for line in list:
        index=index+1
        ahdlogger.warn(f"{line}\n")
        if index<=int(arguments["--lines-skip"]):
            ahdlogger.warn(f"skipping line")
            continue
        if index<=int(arguments["--lines-skip"]):
            ahdlogger.warn(f"skipping line")
            continue
        elif line=='\n' or line=="" or len(line)==0:
            continue

        line=line.rstrip("\n")
        if os.path.isdir(line)==True:
            scan_folder(arguments,line,source)
        elif os.path.isfile(line)==True:
            scan_file(arguments,line,source)
        else:
            currentdate=datetime.now().strftime("%m.%d.%Y_%H%M")
            ahdlogger.warn(f"{line} File or Directory Not found-{currentdate}")
            continue
        print("Waiting 5 Seconds")
        time.sleep(5)
def setup_txt(arguments,interactive=None):
    if interactive==None:
        interactive=False
    file=arguments['--txt']
    try:
        open(file,"a+").close()
    except:
        if interactive==False:
            print("No txt file")
            quit()
        else:
            message_dialog(
                title="Interactive Mode",
                text="Unable to read text file\nPlease Change Config Location\nOr Start Config Wizard",
            ).run()
            return False

def setup_binaries(arguments):
    fdignore=arguments['--fdignore']
    workingdir=os.path.dirname(os.path.abspath(__file__))
    if fdignore==None:
        try:
            arguments['--fdignore']=os.path.join(workingdir,".fdignore")
            t=open(arguments['--fdignore'], 'w')
            t.close()
        except:
            ahdlogger.warn("Error setting up fdignore")
            exit()


    if arguments['--fd']==None and sys.platform=="linux":
        if len(which('fd'))>0:
            arguments['--fd']=which('fd')
        else:
            fd=os.path.join(workingdir,"bin","fd")
            arguments['--fd']=fd

    if arguments['--wget']==None and sys.platform=="linux":
        if len(which('wget'))>0:
            arguments['--wget']=which('wget')
        else:
            ahdlogger.warn("Please Install wget")
            quit()

    if arguments['--fd']==None and sys.platform=="win32":
        if len(which('fd.exe'))>0:
            arguments['--fd']=which('fd')
        else:
            fd=os.path.join(workingdir,"bin","fd.exe")
            arguments['--fd']=fd

    if arguments['--wget']==None and sys.platform=="win32":
        if len(which('wget'))>0:
            arguments['--wget']=which('wget.exe')
        else:
            wget=os.path.join(workingdir,"bin","wget.exe")
            arguments['--fd']=wget
        ahdlogger.warn(arguments['--fd'])
        ahdlogger.warn(arguments['--wget'])
        ahdlogger.warn(arguments['--fdignore'])














"""
Scanning Functions
"""
def set_ignored(arguments):
    ignore=arguments.get("--fdignore")
    if ignore==None or ignore==[] or ignore=="" or len(ignore)==0:
       return
    if type(arguments['--ignore'])==str:
        arguments['--ignore']=arguments['--ignore'].split(",")
    ignorelist=arguments['--ignore']
    if len(ignorelist)==0:
        return
    open(ignore,"w+").close()
    ignore=open(ignore,"a+")
    for element in ignorelist:
        if element=="":
            continue
        ignore.write(element)
        ignore.write('\n')
def searchdir(arguments):
    ignorefile=arguments['--fdignore']
    if arguments['--root']==[] or arguments['--root']==None or len(arguments['--root'])==0:
        return
    #shell=shellbool is true is needed for windows. But cases issues on Linux
    if sys.platform=="linux":
        shellbool=False
    else:
        shellbool=True

    folders=open(arguments['--txt'],"a+")
    ahdlogger.warn("Adding Folders/Files to", arguments['--txt'])
    if type(arguments['--root'])==str:
        arguments['--root']=arguments['--root'].split(",")
    list=arguments['--root']
    for root in list:
        if root=="":
          continue
        if os.path.isdir(root)==False:
          print(root," is not valid directory")
          continue
        t=subprocess.run([arguments['--fd'],'.',root,'-t','d','--max-depth','1','--ignore-file',ignorefile],stdout=subprocess.PIPE,shell=shellbool)
        t2=subprocess.run([arguments['--fd'],'.',root,'-t','f','-e','.mkv','--max-depth','1','--ignore-file',ignorefile],stdout=subprocess.PIPE,shell=shellbool)
        t.stdout=t.stdout.decode('utf8', 'strict')
        t2.stdout=t2.stdout.decode('utf8', 'strict')
        ahdlogger.warn(t.stdout)
        ahdlogger.warn(t2.stdout)
        folders.write(t.stdout)
        folders.write(t2.stdout)
    print("Done")

#Main
if __name__ == '__main__':
    workingdir=os.path.dirname(os.path.abspath(__file__))
    try:
        os.mkdir(os.path.join(workingdir,"Logs"))
    except:
        pass
    arguments = docopt(__doc__, version='ahd_cross_seed_scan 1.5')
    ahdlogger = logging.getLogger('AHD')
    myfilter=filter(arguments)
    ahdlogger.addFilter(myfilter)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler=logging.FileHandler(os.path.join(workingdir,"Logs","ahdupload.logs"))
    filehandler.setFormatter(formatter)
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)

    ahdlogger.addHandler(filehandler)
    ahdlogger.addHandler(streamhandler)

#interactive Mode

    if arguments.get("--config")==None:
        arguments['--config']=os.path.dirname(os.path.abspath(__file__))+"/ahd_cross.txt"
    if (arguments['scan']!=True  and arguments['grab']!=True and arguments['missing']!=True) or arguments['interactive']:
            message_dialog(
                title="Interactive Mode",
                text="Welcome to AHD_Cross_Find you are starting the programs in interactive Mode\nBefore Deciding on the next question note a config File is required in this mode",
            ).run()
            startconfig = button_dialog(
                title="Start Config Wizard",
                buttons=[("Yes", True), ("No", False)],
            ).run()
            if startconfig:
                createconfig(config)
            continueloop =True
            updateargs(arguments)
            setup_binaries(arguments)
            set_ignored(arguments)
            while continueloop!=None:

                continueloop= radiolist_dialog(
                values=[

                    ("download", "Cross Seed Scan"),
                    ("missing", "Upload Finder"),
                    ("scan", "Update Folder/Files"),
                    ("config", "Change Config Location"),
                    ("config2", "Start Config Wizard")
                ],
                title="Interactive Mode",
                text="",
                ).run()
                if continueloop==None:
                    quit()
                elif continueloop=="scan":
                    t=setup_txt(arguments,True)
                    if t==False:
                        continue
                    duperemove(arguments['--fdignore'])
                    searchdir(arguments)
                    duperemove(arguments['--txt'])
                elif continueloop=="missing":
                    t=setup_txt(arguments,True)
                    if t==False:
                        continue
                    setup_binaries(arguments)
                    missing(arguments)
                    duperemove(arguments['--misstxt'])
                elif continueloop=="download":
                    t=setup_txt(arguments,True)
                    if t==False:
                        continue
                    setup_binaries(arguments)
                    download(arguments)
                elif continueloop=="config":
                    arguments['--config']=input_dialog(title='Config Path',text='Please Enter the Path to your Config File:').run()
                    t=setup_txt(arguments,True)
                    if t==False:
                        continue
                    info="Please Check if the arguments are correct for New Config\nIf not their was probably an issue reading the file\nNote all that matters for this mode are the entries with -- at the beginning\n\n"+ str(arguments)
                    message_dialog(
                        title="Options Change",
                        text=info
                    ).run()
                elif continueloop=="config2":
                    createconfig(config)
                    updateargs(arguments)
                    set_ignored(arguments)
                    setup_txt(arguments,True)



#Non interactive Mode
    if arguments['scan']:
        updateargs(arguments)
        setup_txt(arguments)
        setup_binaries(arguments)
        set_ignored(arguments)
        duperemove(arguments['--fdignore'])
        searchdir(arguments)
        duperemove(arguments['--txt'])
    elif arguments['grab']:
        updateargs(arguments)
        setup_txt(arguments)
        setup_binaries(arguments)
        download(arguments)
    elif arguments['missing']:
        updateargs(arguments)
        setup_txt(arguments)
        setup_binaries(arguments)
        missing(arguments)
        duperemove(arguments['--misstxt'])
