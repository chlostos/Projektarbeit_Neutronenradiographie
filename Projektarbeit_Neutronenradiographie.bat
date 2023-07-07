@echo off
@echo ***************************************************************************
@echo ****************          check/ activate conda environment      **********
@echo ****************          start the python script                **********
@echo ***************************************************************************

rem Set the current directory as the script path
set script_path=%cd%

rem Check if the environment.yml file exists
if not exist environment.yml (
    echo ERROR: environment.yml file not found.
    echo Please make sure the file exists in the same directory like this bat and run the script again.
    echo If the file does not exist, you can either download from the git repository or
    echo create a new one by running CreateEnvironmentYml.bat
    pause
    exit /b 1
)

rem Check if the environment.yml file is valid YAML
call findstr /B /C:"name:" environment.yml >nul
if %errorlevel% neq 0 (
    echo ERROR: environment.yml file is not valid YAML.
    echo Please make sure the file is a valid YAML file and run the script again.
    pause
    exit /b 1
)

rem Extract the name of the Anaconda environment from the environment.yml file
for /f "tokens=1,* delims=: " %%i in ('findstr /B "name:" environment.yml') do set env_name=%%j

rem Check if the Anaconda environment exists
call conda info --envs | find "%env_name%" > nul
if %errorlevel% equ 0 (
    rem If the environment exists, activate it and update it
    echo Environment '%env_name%' exists, activating...
    call conda activate %env_name%
    echo Environment '%env_name%' exists, activating...
    echo.
    echo Updating the environment...
    call conda env update -f environment.yml --prune

) else (
    rem If the environment does not exist, create it and activate it
    echo Environment '%env_name%' does not exist, creating...
    call conda env create -f environment.yml -n %env_name%
    call conda activate %env_name%
)

rem Run the main Python script
python %script_path%\main.py

rem Deactivate the Anaconda environment
call conda deactivate

rem Pause before exiting, allowing the user to view any output
pause
exit