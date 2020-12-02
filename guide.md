# Getting Started
## Config vs [Commandline options i.e what appeares when you do -h]
Config is recommend to set a base. With that you only need to call -c [config file path]
However, any commandline option you pick will overide the config option
## Scanning
You need to generate a list of files and Directories. The output is controled by either 
* --txt in the commandline or
* [txt] in the config file
### radarrt
 radarrrt: These type of folders are created by a program like radarr, this scanner could work with other types of directories. But please read to make sure that your directories are compatible. 
 
 #### Scanner info
 * Search for .mkv files
 * Search 2 Levels max within the choosen root folder. I.e the folder itself is root 0, subfolder are 1, a potential .mkv would be level 2
I have /drive/Movies/ with all my movie files. So I choose that as the raddarrt
an example output could be. 
i.e /drive/Movie/2010/ I would need to add each one of those seperatly
 drive/Movies/Eraserhead (1977)/Eraserhead.1977.RERIP.Criterion.BluRay.Remux.1080p.AVC.FLAC.2.0-HiFi.mkv
 /drive/Movies/Escape from the Planet of the Apes (1971)/Escape.From.the.Planet.of.the.Apes.1971.BluRay.Remux.1080p.AVC.DTS-HD.MA.5.1-SCard.mkv
 /drive/Movies/EuroTrip (2004)/Eurotrip 2004 BDRemux 1080p AVC DTS-HD 5.1-HighCode.mkv
 /drive/Movies/Evangelion 1.0 You Are (Not) Alone (2007)/Evangelion - 1.0 - You Are (Not) Alone (2007).mkv
 /drive/Movies/Evangelion 2.0 You Can (Not) Advance (2009)/Evangelion.2.22.You.Can.(Not).Advance.2009.BluRay.1080p.h264.Remux.DTSHDMA-de[42].mkv
 /drive/Movies/Evangelion 3.0 You Can (Not) Redo (2012)/Evangelion.3.33.You.Can.Not.Redo.2012.1080p.BluRay.Remux.TrueHD5.1.H.264-BoxFace.mkv
 /drive/Movies/Eve's Bayou (1997)/Eves_Bayou_1997_1080p_AMZN_WEBRip_DDP2_0_x264-monkee.mkv
 /drive/Movies/Everything Must Go (2010)/Everything.Must.Go.2010.1080p.BluRay.Remux.AVC.DTS-HD.MA.5.1-PmP.mkv
 /drive/Movies/Evil Dead II (1987)/Evil.Dead.2.1987.MULTi.1080p.BluRay.REMUX.AVC.DTS-HDMA.5.1-HDForever.mkv
 /drive/Movies/Evil Eye (2020)/Evil.Eye.2020.NORDiC.1080p.WEB-DL.H.264.DD5.1-TWA.mkv
 /drive/Movies/Evolution (2001)/Evolution.2001.1080i.DTheater.REMUX.MPEG2.DTS5.1-gr0ud3n.mkv
 /drive/Movies/eXistenZ (1999)/eXistenZ.1999.DEU.BluRay.Remux.1080p.AVC.DTS-HD.MA.5.1-TDD.mkv
 /drive/Movies/eXistenZ (1999)/EXistenZ.1999.MULTi.VFF.1080p.BluRay.REMUX.CUSTOM.AVC-Claudeb71.mkv
 /drive/Movies/Extreme Job (2019)/Geukhanjikeob.AKA.Extreme.Job.2019.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-EDPH.mkv
 /drive/Movies/Extremely Wicked, Shockingly Evil and Vile (2019)/Extremely.Wicked.Shockingly.Evil.and.Vile.2019.BluRay.1080p.DTS-HD.HRA.5.1.AVC.REMUX-FraMeSToR.mkv
 /drive/Movies/Eyes Wide Shut (1999)/Eyes Wide Shut 1999 Repack 1080p Blu-ray Remux VC-1 DTS-HD MA 5.1 - KRaLiMaRKo.mkv
 /drive/Movies/Falling Down (1993)/Falling.Down.1993.1080p.Remux.VC-1.TrueHD.2.0-playBD.mkv
 /drive/Movies/Falling Down (1993)/Falling.Down.1993.BluRay.Remux.1080p.VC1.TrueHD.2.0-BMF.mkv
### sonarrt
sonarrt: These type of folders are created by a program like sonnar, teh scanner will look for these type of folders(ending in Season XX), then add that directory to the scanning list
 #### Scanner info
 * Search for folders ending in Season XX
 * Search 2 Levels within the choosen root folder. I.e the folder itself is root 0, show folders are 1, a potential season XX would be level 2
 
 
 I have /drive/TV/ with all my TV files. So I choose that as the sonarrt
an example output could be. 
 /drive/TV/Smallville/Season 01
 /drive/TV/Smallville/Season 02
 /drive/TV/Smallville/Season 03
 /drive/TV/Smallville/Season 04
 /drive/TV/Smallville/Season 05
 /drive/TV/Smallville/Season 06
 /drive/TV/Smallville/Season 07
 /drive/TV/Smallville/Season 08
 /drive/TV/Smallville/Season 09
 /drive/TV/Smallville/Season 10
### normalrtt:
normalrtt: These type of folders will be scan much the same as the ls or dir command. So every file or directory will be added to the scanning list. As they appear in the directory chosen. 
## Grabbing
### Type of checks
Their are two ways for a file/Folder to match one way is for all the information like group resolution source type, etc to match. 
A second way is for just the group and filesize to match. The reason it is not just the filesize, is because sometimes remuxes are basically the same sizes between groups.
A match leads to a download or output line to a file
### Grabbing:Folder vs File
#### Folder
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
## Other
### Missing
How it works is if for example we have a avengers remux, and the site has no avengers remux uploaded, then that will be written to the output2 file.
Also if we have an encode that has not been upload. Even if an encode already exist your encode will be added to the list.
The result is that one will now have an easy to use list of potential files to upload
### Note on Ignore
Ignore is used by fd to find what directories to disregard.
Ignore folders will never be added as a directory during a scan. However sub-folders of a ignore folder be added if the ignore folder is chosen as root. 
If we chose a file to be ignored, then since we can't cd into a file that file will always be ignored. 
### Errors
Their are numerous reason for errors. Somes Python just can't get the size of a file if it is moutned. Other times AHD has network issues, and the api won't work. We try to skip over these errors and move onto the next file. If for some reason something happens. We have the errors file which is created when the program starts, and is updated until it ends.
### Notes
Running this everyday would be excessive especially on a large library. I would recommend using a scheduler. Linux has cron(not a big fan), jobber, cronicle. 
Windows has the task scheduler. With any you used be able to set the program to run every week
### New Feature
 File scan now we can check individual files for matches probably most useful for Movies. With this we are going to change how the scanning option scans radarr type folders to output the individual file, and not the diretory
### Future Feature
Replace all print statements with proper console so user can't select how much to show