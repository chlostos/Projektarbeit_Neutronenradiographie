@echo off
@echo ***************************************************************************
@echo ****************          Project Start manager           *****************
@echo ***************************************************************************
@echo !! if you are implementing the batch startup wrapper for your project you need to           !!
@echo !! search and replace "project-Python" string in the startup batch file  with a unique name !!
@echo Started @ %date% %time%
@echo * check if the Projektarbeit_Neutronenradiographie is already up and running:
@echo ** wait some random time to avoid multi start clashes of the script

set /a rand=%random% %%26+5
timeout /t %rand%

@echo * check active tasks if the batch we are starting is already running:
@echo 1st - generate a random file name to store task check
FOR /F "delims=" %%i IN ('get_random_string.bat') DO set file_name=%%i
set "file_name=tasklist_%file_name%.txt"
@echo 2nd - pipe tasklist to random file name
tasklist /v > %file_name%
@echo 3rd - search for named batch "Projektarbeit_Neutronenradiographie" in the file with the random name
findstr /m /c:"Projektarbeit_Neutronenradiographie" %file_name%
@echo 4th if string was found quit the batch, otherwise call the target *.bat file
@IF ERRORLEVEL 1 (
   del %file_name%
@  echo 4a - No running instance is found - starting project python script.
   start "Projektarbeit_Neutronenradiographie" /Min Projektarbeit_Neutronenradiographie.bat
   timeout /t 10
   echo project started
) ELSE (
   del %file_name%
@  echo 4b Projektarbeit_Neutronenradiographie is already running!
)
@echo Ended: %date% %time%
timeout /t 10