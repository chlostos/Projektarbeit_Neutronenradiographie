@echo off
@echo check if Anaconda is installed
@echo exit if not
@echo if yes, check that Projektarbeit_Neutronenradiographie environment is installed
@echo or install it
@ set "ifErr=set foundErr=1&(if errorlevel 0 if not errorlevel 1 set foundErr=)&if defined foundErr"
(
  @ conda info --envs > %temp%\conda_env.txt
  %ifErr% ( echo no conda found, use AMStore to install Anaconda
            pause
            exit
            )
  findstr /c:"Projektarbeit_Neutronenradiographie" %temp%\conda_env.txt && (
  echo conda environment found ) || (
  echo conda environment missing, start creation process
  conda env create -f environment.yml
  )
)