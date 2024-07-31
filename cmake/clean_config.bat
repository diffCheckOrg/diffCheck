REM activate the conda diff_check environment otherwise the python wrap won't work
call cmake/activate_conda.bat

REM clean the build directory and reconfigure it
rmdir /s /q build

REM configure the project
conda run --name diff_check --no-capture-output  cmake -S . -B build -DCMAKE_BUILD_TYPE=Release