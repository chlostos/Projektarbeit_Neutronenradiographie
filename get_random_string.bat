@echo off
rem Turn off echoing of commands
rem Create random strings for e.g. random filenames

rem ***** MAIN PART *****
rem Enable delayed expansion of variables
setlocal enabledelayedexpansion

rem 1st set variables:
rem Set the string of characters to use for generating random strings
set "string=abcdefghijklmnopqrstuvwxyz"
rem Set the maximum number for the randomizer based on the length of the string
call :strlen string
set /a max=%len%
rem Initialize the variable that will hold the generated random string
set "result="


rem 2. create the string
rem loop to create a 30 digit random string:
for /L %%i in (1,1,30) do call :add
rem Generate a random string by calling the :add subroutine 30 times

rem 3. print string to console
rem Echo the generated random string to the console
echo %result%
rem 4. Exit the script
goto :eof

rem *******************************************
rem ***** subroutines starting here ***********
rem *******************************************

rem Subroutine for generating a random letter and appending it to the result variable
:add
set /a x=%random% %% %max%
rem Generate a random number between 0 and the maximum number to select a letter from the string
set result=%result%!string:~%x%,1!
rem Append the selected letter to the result variable
goto :eof
rem Return to the main code


rem Subroutine for getting the length of a string
:strlen
rem Get the input string
set "s=%*"
rem Initialize the length variable
set "len=0"
rem Count the length of the string
:loop
if defined s (
set "s=%s:~1%"
set /a "len+=1"
goto :loop
)
rem Return to the main code
goto :eof