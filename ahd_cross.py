#! /usr/bin/env python3
"""NOTE: READ DOCUMENTATION BEFORE USAGE.
Usage:
    ahd_cross.py (-h | --help)
    ahd_cross.py scan [--txt=<txtlocation>]
    [--radarrt <movie_root(s)>]... [--sonarrt <tv_root(s)>]... [--normalrt <normal_root(s)>]... [--ignore <sub_folders_to_ignore>]...
    [--config <config>][--delete][--fd <b--inary_fd> --fdignore <gitignore_style_ignorefile> ]
    ahd_cross.py grab [--txt=<txtloc--ation>][--torrent <torrents_download> --cookie <cookie> --output <output> --api <apikey>]
    [--config <config>][--date <int> --fd <binary_fd> --size <t_or_f>][--exclude <source_excluded>]...
    ahd_cross.py missing [--txt=<txtlocation> --output2 <output>  --api <apikey>][--config <config>]
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
  --torrent ; -t <torrents_download>  Here are where the torrent files will download
  --cookie ; -c <cookie> This is a cookie file for ahd, their are numerous extensions to grab this.
  --output ; -o <output>  Here are where the torrentlinks will be weritte
  --date ; -d <int> only download torrents newer then this input should be int, and represents days. By default it is set to around 25 years(optional)  [default: 10000 ]
  --api ; -a <apikey> This is your ahd passkey
  --exclude ; -e <source_excluded>  These file type(s) will not be scanned blu,tv,remux,other,web.(optional)
  --size ; -s <t_or_f> set whether a search should be done by name only or include file size restriction. If true then secondary check will be added to find a match [default: t]
  "1080p Remux Files,2160 Remux Files or etc files" in a directory match the size of the ahd response(optional)   [default: 1]

  ahd_cross.py missing
  --output2 <txt_where_potential_uploads_are written> here we output to a txt file files that don't have any uploads. This means that we can potentially upload these, for rank. Or to increase the amount of cross seeds we have


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
config = configparser.ConfigParser(allow_no_value=True)
#import other files
from folders import *
from classes import *
from files import *



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
def createconfig(arguments):
    try:
        configpath=arguments.get('--config')
        config.read(configpath)
    except:
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
    if arguments['--output2']==None:
        arguments['--output2']=config['grab']['output2']
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
    for element in arguments['--exclude']:
        try:
            source[element]="No"
        except KeyError:
            pass
    return source
def download(arguments,txt):
    list=open(txt,"r")
    source=releasetype(arguments)
    errorfile=errorpath=pathlib.Path(__file__).parent.absolute().as_posix()+"/Errors/"
    if os.path.isdir(errorfile)==False:
            os.mkdir(errorfile)
    errorfile=errorfile+"ahdcross_errors_"+datetime.now().strftime("%m.%d.%Y_%H%M")+".txt"
    for line in list:
        print('\n',line)
        if line=='\n' or line=="" or len(line)==0:
            continue
        line=line.rstrip("\n")
        if os.path.isdir(line)==True:
            download_folder(arguments,txt,line,source,errorfile)
        else:
            print("false")
            download_file(arguments,txt,line,source,errorfile)
        print("Waiting 5 Seconds")
        time.sleep(5)
def scan(arguments,txt):
    source=releasetype(arguments)
    list=open(txt,"r")
    errorfile=pathlib.Path(__file__).parent.absolute().as_posix()+"/Errors/"
    if os.path.isdir(errorfile)==False:
            os.mkdir(errorfile)
    errorfile=errorfile+datetime.now().strftime("%m.%d.%Y_%H%M")+".txt"

    for line in list:
        print('\n',line)
        if line=='\n':
            continue
        line=line.rstrip("\n")
        if os.path.isdir(line)==True:
            scan_folder(arguments,txt,line,source,errorfile)
        else:
            scan_file(arguments,txt,line,source,errorfile)
        print("Waiting 5 Seconds")
        time.sleep(5)
"""
Scanning Functions
"""
def set_ignored(arguments,ignore):
    if ignore==None:
       return
    try:
        ignorelist=arguments['--ignore'].split(',')
    except:
         ignorelist=arguments['--ignore']
    if len(ignorelist)==0:
        return
    open(ignore,"w+").close()
    ignore=open(ignore,"a+")
    for element in ignorelist:
        ignore.write(element)
        ignore.write('\n')
def searchtv(arguments,ignorefile):
  if arguments['--sonarrt']==[] or arguments['--sonarrt']==None or len(arguments['--sonarrt'])==0:
      return
  folders=open(arguments['--txt'],"a+")
  print("Adding TV Folders to",arguments['--txt'])
  try:
    list=arguments['--sonarrt'].split(',')
  except:
    list=arguments['--sonarrt']
  for root in list:
      if os.path.isdir(root)==False:
          print(root," is not valid directory")
          continue
      subprocess.run([arguments['--fd'],'Season\s[0-9][0-9]$','-t','d','--full-path',root,'--ignore-file',ignorefile],stdout=folders)
  print("Done")
def searchmovies(arguments,ignorefile):
    print(arguments['--radarrt'])
    if arguments['--radarrt']==[] or arguments['--radarrt']==None or len(arguments['--radarrt'])==0:
        return
    folders=open(arguments['--txt'],"a+")
    print("Adding Movies Folders to", arguments['--txt'])
    try:
        list=arguments['--radarrt'].split(',')
    except:
        list=arguments['--radarrt']
    for root in list:
        if os.path.isdir(root)==False:
          print(root," is not valid directory")
          continue
    subprocess.run([arguments['--fd'],'\)$','-t','d','--full-path',root,'--ignore-file',ignorefile],stdout=folders)
    print("Done")
def searchnormal(arguments,ignorefile):
    workingdir=os.getcwd()
    if arguments['--normalrt']==[] or arguments['--normalrt']==None:
        return
    folders=open(arguments['--txt'],"a+")
    print("Adding Normal Folders to", arguments['--txt'])
    try:
        list=arguments['--normalrt'].split(',')
    except:
        list=arguments['--normalrt']
    for root in list:
        if os.path.isdir(root)==False:
          print(root," is not valid directory")
          continue
        os.chdir(root)
        subprocess.run([arguments['--fd'],'.',root,'-t','d','--max-depth','1','--ignore-file',ignorefile],stdout=folders)
        subprocess.run([arguments['--fd'],'.',root,'-t','f','-e','.mkv','--max-depth','1','--ignore-file',ignorefile],stdout=folders)
    print("Done")
    os.chdir(workingdir)
if __name__ == '__main__':
    arguments = docopt(__doc__, version='ahd_cross_seed_scan 1.2')
    createconfig(arguments)
    file=arguments['--txt']
    try:
        open(file,"a+").close()
    except:
        print("No txt file")
        quit()
    if arguments['scan']:
        print("Scanning for folders")
        if arguments['--delete']:
            open(file, 'w').close()
        fdignore=arguments['--fdignore']
        if fdignore==None:
            try:
                fdignore=os.environ['HOME'] + "/.fdignore"
            except:
                print("You might be on windows make sure to pass --fdignore option")
                exit()
        duperemove(fdignore)
        searchtv(arguments,fdignore)
        searchmovies(arguments,fdignore)
        searchnormal(arguments,fdignore)
        duperemove(arguments['--txt'])
    elif arguments['grab']:
        download(arguments,file)
    elif arguments['missing']:
        if arguments['--output2']=='':
            print("output2 must be configured for missing scan ")
            quit()
        scan(arguments,file)
        duperemove(arguments['--output2'])
    elif arguments['dedupe']:
        duperemove(arguments['--txt'])
