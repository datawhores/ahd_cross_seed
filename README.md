# Install
### Clone the repository
git clone https://gitlab.com/excludedBittern8/ahd_cross_seed

cd ahd_cross_seed

### Creating a virtual enviroment
A Virtual environment is recommended. Please Make sure you are on python3 and NOT python 2

On macOS and Linux:
python3 -m pip install --user virtualenv

On Windows:
py -m pip install --user virtualenv

##### Add required modules
./venv/bin/pip3 install -r requirements.txt

##### running python from venv
./venv/bin/python

on Windows
./venv/bin/python.exe

# Quick Guide``
Please start here for a general overview of how to run this program. 
### Scanning Directory

`ahd_cross.py scan [arguments]` 

scan a directory will write the paths to a txt document
    required
    --txt this is where the txt file will be saved
    
    optional
    --delete ; -d This will delete the txt file otherwise the file is just appeneded
    --exclude ; -e Exclude certain types of videos from being added to txt file blu=encode,remux=remux,web=web-dl or web-rip orweb,tv=hdtv,other=badly named files
    --ignored ; -i this folder will be ignored completly, appends to .fdignore, so this should only need to be done once. 

### Grabbing Downloads
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

### Find Files to Upload to AHD
`ahd_cross.py missing [arguments]`

Will scan a directory and find any file that hasn't been uploaded to AHD. That also has a free slot on AHD. Any encode that hasn't been uploaded will be added 
    required
    --missingtxt write paths to this txt file
    --api ; -a  your passkey key

    optional
    [--exclude <source_excluded>... For any directory this type of file will not be checked for possible cross seeds

### interactive
`ahd_cross.py [arguments]` or `ahd_cross.py interactive [arguments]` 
Start a gui version of the program






















# Arguments 
A more in-depth overview of some of the argument that can be passed to the program

### Config vs arguments
Config is recommend to set a base. With that you only need to call -c [config file path]
However, any commandline option you pick will overide the config option


#### scan
`ahd_cross.py scan [arguments]` 
You need to generate a list of files and Directories. The output is controled by either 
* --txt in the commandline or
* [txt] in the config file

#### --root:
This  folder(s) will be scan much the same as the ls or dir command. So every file or directory will be added to the scanning list. As they appear in the directory chosen. 

Note: If you have a sonnar or raddar file please check these repos out [placeholder]

### grab
`ahd_cross.py grab [arguments]` 

You will need to provide a txt file of directories/folders. Either generated manually or with the scan command
### Type of checks

Their are two ways for a file/Folder to match one way is for all the information like group resolution source type, etc to match. 
Alternatively second way is for just the group and filesize to match. The reason it is not just the filesize, is because sometimes remuxes are basically the same sizes between groups. The Second check is toggle off and on by the --size argument

If all values match, then the file is downloaded

#### Folder vs File
##### Folder
When the grabber sees a folder in the txt list. It will start a folder scan.
This should normally only apply to TV folders
A folder scan will scan every type of file i.e web-dl web-rip individually. The size calculated will be based on that type of file. This goes down to the resolution so 
* WEB-Dl 1080p
* WEB-DL 2160p 
will both be consider to be two different release. However if you had 
* Framestor 1080p Remux
* Epislon 1080p Remux in the same folder. 
That could lead to issues as now the sescond type of matching would not work. As the size match would be off

#### File
File scans are much the same as folder scan. If the information matches then the torrent is downloaded or output to file. However the check is based on the path on the txt file


### missing

How it works is if for example we have a avengers remux, and the site has no avengers remux uploaded, then that will be written to the misstxt file.
Also if we have an encode that has not been upload. Even if an encode already exist your encode will be added to the list.
The result is that one will now have an easy to use list of potential files to upload

### Other
#### --ignore
Ignore is used by fd to find what directories to disregard.
Ignore folders will never be added as a directory during a scan. However sub-folders of a ignore folder be added if the ignore folder is chosen as root. 
If we chose a file to be ignored, then since we can't cd into a file that file will always be ignored. 


#### Errors
Their are numerous reason for errors. Somes Python just can't get the size of a file if it is moutned. Other times AHD has network issues, and the api won't work. We try to skip over these errors and move onto the next file. If for some reason something happens. We have the errors file which is created when the program starts, and is updated until it ends.

#### Courtesy
Running this everyday would be excessive especially on a large library. I would recommend using a scheduler. Linux has cron(not a big fan), jobber, cronicle. 
Windows has the task scheduler. With any you used be able to set the program to run every week



   
    
    
    
    
    
    
 
    
    
    
    


