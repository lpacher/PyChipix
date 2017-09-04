
@echo off


:: parse here the command line help
if "%1"=="--help" (

   echo.
   echo Command line usage:
   echo.
   echo pychipix [[--batch^|--gui] ^| [script.py]]
   echo.
   echo Options:
   echo.
   echo  --batch : run in batch mode without graphics
   echo  --gui   : start interactive session and open the TControlBar 
   echo.

   goto end

) else (

   goto start

)


:start

python -i -O pychipix %* || exit

:end
