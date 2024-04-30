@echo off
setlocal

REM activate the conda diff_check environment otherwise the python wrap won't work
call cmake/activate_conda.bat

REM build the project in Release mode
cmake --build build --config Release