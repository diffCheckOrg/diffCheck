@echo off
setlocal

REM activate the conda diff_check environment otherwise the python wrap won't work
call cmake/activate_conda.bat

REM configure the project
cmake -S . -B build -G "Visual Studio 16 2019" -A x64