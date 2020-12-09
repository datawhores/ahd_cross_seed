#! /usr/bin/env python3
"""NOTE: READ DOCUMENTATION BEFORE USAGE.
Usage:
    ahd_cross.py
    ahd_cross.py (-h | --help)
    ahd_cross.py scan [--txt=<txtlocation>]
    [--radarrt <movie_root(s)>]... [--sonarrt <tv_root(s)>]... [--normalrt <normal_root(s)>]... [--ignore <sub_folders_to_ignore>]...
    [--config <config>][--delete][--fd <b--inary_fd> --fdignore <gitignore_style_ignorefile> ]
    ahd_cross.py grab [--txt=<txtloc--ation> --lines-skip <num_lines_skipped>][--torrent <torrents_download> --cookie <cookie> --output <output> --api <apikey>]
    [--config <config>][--date <int> --fd <binary_fd> --size <t_or_f>][--exclude <source_excluded>]...
    ahd_cross.py missing [--txt=<txtlocation> --misstxt <output>  --api <apikey>][--config <config>]
    ahd_cross.py dedupe --txt=<txtlocation>





Options:
  -h --help     Show this screen.
 --txt <txtlocation>  txt file with all the file names(required for all commands)
--fd <binary_fd> fd is a program to scan for files, use this if you don't have fd in path,(optional)   [default: fd]
--config ; -x <config> commandline overwrites config
--fdignore <gitignore_style_ignorefile> fd .fdignore file used by fd tto find which folders to ignore, on linux it defaults to the home directory.
other OS may need to input this manually


 ahd_cross.py scan scan tv or movie folders root folder(s) create a list of directories. 'txt file creator'. Need at least 1 root.
--sonarrt <tv_root(s)> These are sonnarr type folders with the files with in a "season **" type folders. Will only write directories
--radarrt <movie_root(s)> These are radarr type folders with the files in a file that ends in the year. Will only write directories
--normalrt <normal_root(s)> This Types of folders are not radarr or sonarr folders. Every Item in this folder will be added to the scan list. Max depth of 1
--delete; -d  Will delete the old txt file(optional)
--ignore ; -i <sub_folders_to_ignore>  folder will be ignored for scan (optional)


 ahd_cross.py grab downloads torrents using txt file option to download torrent with --cookie and/or output to file.
  --lines-skip <num_lines_skipped> Number of lines in txt file to skip during grab  [default: 0]
  --torrent ; -t <torrents_download>  Here are where the torrent files will download
  --cookie ; -c <cookie> This is a cookie file for ahd, their are numerous extensions to grab this.
  --output ; -o <output>  Here are where the torrentlinks will be weritte
  --date ; -d <int> only download torrents newer then this input should be int, and represents days. By default it is set to around 25 years(optional)  [default: 10000 ]
  --api ; -a <apikey> This is your ahd passkey
  --exclude ; -e <source_excluded>  These file type(s) will not be scanned blu,tv,remux,other,web.(optional)
  --size ; -s <t_or_f> set whether a search should be done by name only or include file size restriction. If true then secondary check will be added to find a match [default: t]
  "1080p Remux Files,2160 Remux Files or etc files" in a directory match the size of the ahd response(optional)   [default: 1]

  ahd_cross.py missing
  --misstxt <txt_where_potential_uploads_are written> here we output to a txt file files that don't have any uploads. This means that we can potentially upload these, for rank. Or to increase the amount of cross seeds we have


  ahd_cross.py dedupe
  Just a basic script to remove duplicate entries from the list. scan will automatically run this after it finishes

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



"""
Setup Function
"""

def duperemove(txt):
    print("Removing Duplicate lines from ",txt)
    if txt==None:
        return
    input=open(txt,"r")
    lines_seen = set() # holds lines already seen
    for line in input:
        if line not in lines_seen: # not a duplicate
            lines_seen.add(line)
    input.close()
    outfile = open(txt, "w")
    for line in lines_seen:
        outfile.write(line)
    outfile.close()
def updateargs(arguments):
    try:
        configpath=arguments.get('--config')
        config.read(configpath)
    except:
        print("Could Not Read Config Path")
        return arguments
    if arguments['--txt']==None:
        arguments['--txt']=config['general']['txt']
    if arguments['--fd']=="fd":
        arguments['--fd']=config['general']['fd']
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
    if arguments['--radarrt']==[] or  arguments['--radarrt']==None:
        arguments['--radarrt']=config['scan']['radarrt']
    if arguments['--sonarrt']==[] or  arguments['--sonarrt']==None:
        arguments['--sonarrt']=config['scan']['sonarrt']
    if arguments['--normalrt']==[] or  arguments['--normalrt']==None:
        arguments['--normalrt']=config['scan']['normalrt']
    if arguments['--ignore']==[] or arguments['--ignore']==None:
        arguments['--ignore']=config['scan']['ignore']
    if arguments['--size']=="1":
        arguments['--size']=config['grab']['size']
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
    return source
def download(arguments,txt):
    index=0
    list=open(txt,"r")
    source=releasetype(arguments)
    errorfile=errorpath=pathlib.Path(__file__).parent.absolute().as_posix()+"/Errors/"
    if os.path.isdir(errorfile)==False:
            os.mkdir(errorfile)
    errorfile=errorfile+"ahdcross_errors_"+datetime.now().strftime("%m.%d.%Y_%H%M")+".txt"
    for line in list:
        index=index+1
        print('\n',line)
        if index<=int(arguments["--lines-skip"]):
            print("Skipping Line")
            continue
        if line=='\n' or line=="" or len(line)==0:
            continue
        line=line.rstrip("\n")


        if os.path.isdir(line)==True:
            download_folder(arguments,txt,line,source,errorfile)
        elif os.path.isfile(line)==True:
            download_file(arguments,txt,line,source,errorfile)

        else:
            print("File or Dir Not found")
            errorpath=open(errorfile,"a+")
            errorstring=line +": File or Dir Not found "  + " - " +datetime.now().strftime("%m.%d.%Y_%H%M") + "\n"
            errorpath.write(errorstring)
            errorpath.close()
            continue
        print("Waiting 5 Seconds")
        time.sleep(5)
def missing(arguments):
    if arguments['--misstxt']=='' or len(arguments['--misstxt'])==0 or arguments['--misstxt']==None:
        print("misstxt must be configured for missing scan ")
        quit()
    source=releasetype(arguments)
    list=open(arguments['--txt'],"r")
    index=0
    errorfile=pathlib.Path(__file__).parent.absolute().as_posix()+"/Errors/"
    if os.path.isdir(errorfile)==False:
            os.mkdir(errorfile)
    errorfile=errorfile+datetime.now().strftime("%m.%d.%Y_%H%M")+".txt"
    for line in list:
        index=index+1
        print('\n',line)
        if index<=int(arguments["--lines-skip"]):
            print("Skipping Line")
            continue
        elif line=='\n' or line=="" or len(line)==0:
            continue
        if  re.search("#",line)!=None:
            print("Skipping Line")
            continue
        line=line.rstrip("\n")

        if os.path.isdir(line)==True:
            scan_folder(arguments,line,source,errorfile)
        elif os.path.isfile(line)==True:
            scan_file(arguments,line,source,errorfile)
        else:
            print("File or Dir Not found")
            errorpath=open(errorfile,"a+")
            errorstring=line +": File or Dir Not found "  + " - " +datetime.now().strftime("%m.%d.%Y_%H%M") + "\n"
            errorpath.write(errorstring)
            errorpath.close()
            continue

        print("Waiting 5 Seconds")
        # time.sleep(5)
def setup(arguments):
    updateargs(arguments)
    file=arguments['--txt']
    os.chdir(Path.home())
    try:
        open(file,"a+").close()
    except:
        print("No txt file")
        quit()
def setupscan(arguments):
    print("Scanning for folders")
    if arguments['--delete']:
        open(file, 'w').close()
    fdignore=arguments['--fdignore']
    if fdignore==None:
        try:
            arguments['--fdignore']=os.path.dirname(os.path.abspath(__file__))+ "/.fdignore"
        except:
            print("Error setting fdignore")
            exit()
    t=open(arguments['--fdignore'], 'w')
    t.close()

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
def searchtv(arguments,ignorefile):
  workingdir=os.getcwd()
  if arguments['--sonarrt']==[] or arguments['--sonarrt']==None or len(arguments['--sonarrt'])==0:
      return
  folders=open(arguments['--txt'],"a+")
  print("Adding TV Folders to",arguments['--txt'])
  if type(arguments['--sonarrt'])==str:
      arguments['--sonarrt']=arguments['--sonarrt'].split(",")
  list=arguments['--sonarrt']
  for root in list:
      if root=="":
          continue
      if os.path.isdir(root)==False:
          print(root," is not valid directory")
          continue
      t=subprocess.run([arguments['--fd'],'Season\s[0-9][0-9]$','-t','d','.',root,'--max-depth','2','--min-depth','2','--ignore-file',ignorefile],stdout=folders)
  print("Done")
def searchmovies(arguments,ignorefile):
    workingdir=os.getcwd()
    if arguments['--radarrt']==[] or arguments['--radarrt']==None or len(arguments['--radarrt'])==0:
        return
    folders=open(arguments['--txt'],"a+")
    print("Adding Movies Folders to", arguments['--txt'])
    if type(arguments['--radarrt'])==str:
        arguments['--radarrt']=arguments['--radarrt'].split(",")
    list=arguments['--radarrt']
    for root in list:
        if root=="":
          continue
        if os.path.isdir(root)==False:
          print(root," is not valid directory")
          continue
    #old scanning method
    #subprocess.run([arguments['--fd'],'\)$','-t','d','--full-path',root,'--ignore-file',ignorefile],stdout=folders)
        t=subprocess.run([arguments['--fd'],'-e','.mkv','-t','f','.',root,'--max-depth','2','--ignore-file',ignorefile],stdout=folders)
    print("Done")
def searchnormal(arguments,ignorefile):
    if arguments['--normalrt']==[] or arguments['--normalrt']==None:
        return
    folders=open(arguments['--txt'],"a+")
    print("Adding Normal Folders to", arguments['--txt'])
    if type(arguments['--normalrt'])==str:
        arguments['--normalrt']=arguments['--normalrt'].split(",")
    list=arguments['--normalrt']
    for root in list:
        if root=="":
          continue
        if os.path.isdir(root)==False:
          print(root," is not valid directory")
          continue
        subprocess.run([arguments['--fd'],'.',root,'-t','d','--max-depth','1','--ignore-file',ignorefile],stdout=folders)
        subprocess.run([arguments['--fd'],'.',root,'-t','f','-e','.mkv','--max-depth','1','--ignore-file',ignorefile],stdout=folders)
    print("Done")

#Main
if __name__ == '__main__':
    arguments = docopt(__doc__, version='ahd_cross_seed_scan 1.2')
#interactive Mode

    if arguments.get("--config")==None:
        arguments['--config']=os.path.dirname(os.path.abspath(__file__))+"/ahd_cross.txt"
    if arguments['scan']!=True and arguments['dedupe']!=True and arguments['grab']!=True and arguments['missing']!=True:
            message_dialog(
                title="Interactive Mode",
                text="Welcome to AHD Cross you are starting the programs in interactive Mode\nBefore Deciding on the next question note a config File is required in this mode",
            ).run()
            startconfig = button_dialog(
                title="Start Config Wizard",
                buttons=[("Yes", True), ("No", False)],
            ).run()
            if startconfig:
                createconfig(config)
            continueloop =True
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
                    setup(arguments)
                    setupscan(arguments)
                    set_ignored(arguments)
                    duperemove(arguments['--fdignore'])
                    searchtv(arguments,arguments['--fdignore'])
                    searchmovies(arguments,arguments['--fdignore'])
                    searchnormal(arguments,arguments['--fdignore'])
                    duperemove(arguments['--txt'])
                elif continueloop=="missing":
                    setup(arguments)
                    missing(arguments)
                    duperemove(arguments['--misstxt'])
                elif continueloop=="download":
                    setup(arguments)
                    download(arguments,arguments['--txt'])
                elif continueloop=="config":
                    arguments['--config']=input_dialog(title='Config Path',text='Please Enter the Path to your Config File:').run()
                    setup(arguments)
                    info="Please Check if the arguments are correct for New Config\nIf not their was probably an issue reading the file\nNote all that matters for this mode are the entries with -- at the beginning\n\n"+ str(arguments)
                    message_dialog(
                        title="Options Change",
                        text=info
                    ).run()
                elif continueloop=="config2":
                    createconfig(config)



#Non interactive Mode
    if arguments['scan']:
        setup(arguments)
        setupscan(arguments)
        set_ignored(arguments)
        duperemove(arguments['--fdignore'])
        searchtv(arguments,arguments['--fdignore'])
        searchmovies(arguments,arguments['--fdignore'])
        searchnormal(arguments,arguments['--fdignore'])
        duperemove(arguments['--txt'])
    elif arguments['grab']:
        setup(arguments)
        download(arguments,arguments['--txt'])
    elif arguments['missing']:
        setup(arguments)
        missing(arguments)
        duperemove(arguments['--misstxt'])
    elif arguments['dedupe']:
        duperemove(arguments['--txt'])
