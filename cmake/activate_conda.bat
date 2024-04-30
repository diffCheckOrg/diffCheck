@echo off
setlocal

REM ########################################################################
REM check if conda is available > 
REM check that diff_check environment is available > 
REM activate it
REM ########################################################################

REM Check if conda command is available
echo Checking if conda command is available...
where conda >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Conda command is available.
    goto :end
)
if exist "%USERPROFILE%\Anaconda3" (
    echo Anaconda3 found in %USERPROFILE%\Anaconda3.
    goto :end
)
if exist "%ProgramData%\Anaconda3" (
    echo Anaconda3 found in %ProgramData%\Anaconda3.
    goto :end
)
if exist "%ProgramFiles%\Anaconda3" (
    echo Anaconda3 found in %ProgramFiles%\Anaconda3.
    goto :end
)
echo Anaconda3 not found, you won't be able to build the python wrap for diffcheck. Please install it first.
exit /b 1

:end
echo Anaconda3 found.

REM Check if the diff_check environment is available
call conda env list | findstr /C:"diff_check" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo diff_check environment not found, creating it now...

    call conda env create -f environment.yml
    if %ERRORLEVEL% neq 0 (
        echo Failed to create diff_check environment, please check the environment.yml file.
        exit /b 1
    )
) else (
    echo diff_check environment is available, updating it now...

    call conda env update --name diff_check --file environment.yml --prune
    if %ERRORLEVEL% neq 0 (
        echo Failed to update diff_check environment, please check the environment.yml file.
        exit /b 1
    )
)
echo diff_check environment is up to date.

REM activate the diff_check environment
call conda activate diff_check
echo diff_check environment activated.