# ahd_cross_seed
**Requirements:**

Python 3

Modules
- requests
- guessit
- docopt
- xmltodict
- IMDbPY
- prompt_toolkit

https://github.com/sharkdp/fd/releases - Note: Instructions say you need root to install the binary. But you don't need root to run it so I've included a version of it in the repo

Windows Users: Please follow the instructions on how to install fd on windows, on the link above

Seedbox Users:

python3 -m venv /path/to/new/virtual/environment then you can use do something like 
/path/to/new/virtual/environment/pip install to install modules and
/path/to/new/virtual/environment/python3 to run the program

# Getting Started:Quick Guide
## Scanning Directory

`ahd_cross.py scan [arguments]` 

scan a directory will write the paths to a txt document
    required
    --txt this is where the txt file will be saved
    
    optional
    --delete ; -d This will delete the txt file otherwise the file is just appeneded
    --exclude ; -e Exclude certain types of videos from being added to txt file blu=encode,remux=remux,web=web-dl or web-rip orweb,tv=hdtv,other=badly named files
    --ignored ; -i this folder will be ignored completly, appends to .fdignore, so this should only need to be done once. 

## Grabbing Downloads
`ahd_cross.py grab [arguments]` 

grab downloads using a list of the directories/files. Files can be generated manually or with this programs scanning function. If Scanning please note that 

    
    [Must pick at least 1]
    --torrent ; -t this is where matching files will be saved
    --output ; -o
    
    required
    --txt find files in folders, searches for possible cross seeds
    --api ; -a  your passkey key

    optional
    --date  restrict downloads only newer then this amount of days, should be an int
    --size ; -z  set whether a search should be done by name only or include file size restriction. If true then an additonal check will be added to see if all the matching
    --exclude ; -e For any directory this type of file will not be checked for possible cross seeds
    --fd fd is a program for finding files if you can't install to system path you can put the location of the binary using this option. Note: a binary is included in this repo

## Find Files to Upload to AHD
`ahd_cross.py missing [arguments]`

Will scan a directory and find any file that hasn't been uploaded to AHD. That also has a free slot on AHD. Any encode that hasn't been uploaded will be added
 
    
    required
    --missingtxt write paths to this txt file
    --api ; -a  your passkey key

    optional
    [--exclude <source_excluded>... For any directory this type of file will not be checked for possible cross seeds


```



   
    
    
    
    
    
    
 
    
    
    
    


