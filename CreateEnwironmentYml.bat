@echo off
@echo Batch Create Environment.yml
@echo -----------------------------
@echo The purpose of this batch is to create an environment.yml file based on your active environment
@echo ...............................................................................................
setlocal
REM Ask if existing files will be overwritten
:PROMPT
SET /P CONFIRM_OVERWRITE=Are you sure that you want to proceed to create an file environment.yml (existing files will be overwritten)  (Y/[N])?
IF /I "%CONFIRM_OVERWRITE%" NEQ "Y" GOTO END

REM Export the environment to a temporary file
conda env export --no-builds --channel conda-forge --channel anaconda-fusion --channel defaults| findstr -v "prefix" > tmp1_environment.yml

REM remove the artifactory (jfrog) line -  so that we can synch the environment to the git
type tmp1_environment.yml | findstr /v /c:"https://" > tmp_environment.yml
type tmp_environment.yml | findstr /v /c:"- /" > environment.yml

REM delete the temp file
del tmp_environment.yml
del tmp1_environment.yml

:END
@echo you reached the end of the batch
endlocal
timeout /T 5