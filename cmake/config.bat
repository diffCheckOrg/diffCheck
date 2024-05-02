REM activate the conda diff_check environment otherwise the python wrap won't work
call cmake/activate_conda.bat

REM configure the project
cmake -S . -B build