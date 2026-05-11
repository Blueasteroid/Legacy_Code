@echo off

@echo Started: %date% %time%

del "temp_filelist.txt" 2> nul

for /f "tokens=*" %%G IN ('dir %1\*.avi /s /b /a-d') DO echo file '%%G' 
for /f "tokens=*" %%G IN ('dir %1\*.avi /s /b /a-d') DO echo file '%%G' >> temp_filelist.txt

@echo TXT saved.
TIMEOUT /T 1

ffmpeg.exe -y -f concat -safe 0 -i temp_filelist.txt -c copy merged.avi
ffmpeg.exe -y -i merged.avi -vcodec libx265 -crf 28 output.mp4

@echo ALL DONE.

@echo Completed: %date% %time%
