@echo off
setlocal

:: run the following in a pop up window to avoid the console window and ask to ru n ass admin
@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------



:: Define the download URL and the target directory
set "url=https://github.com/isl-org/Open3D/releases/download/v0.18.0/open3d-devel-windows-amd64-0.18.0.zip"
set "targetDir=C:\Program Files\Open3Dtest"

:: Create the if the directory does not exist
if not exist "%targetDir%" mkdir "%targetDir%

:: check if the directory was created
if not exist "%targetDir%" (
    echo Failed to create the target directory.
    exit /b 1
)

:: Download the file
echo Downloading Open3D...
curl -L -o "%targetDir%\open3d.zip" "%url%"

:: Check if the file was downloaded
if not exist "%targetDir%\open3d.zip" (
    echo Failed to download Open3D.
    exit /b 1
)

:: Extract the file
echo Extracting Open3D...
powershell -Command "Expand-Archive -Path '%targetDir%\open3d.zip' -DestinationPath '%targetDir%'"

@REM :: Delete the downloaded zip file
@REM del "%targetDir%\open3d.zip"

@REM :: Change to the target directory
@REM cd /d "%targetDir%"

@REM :: Run the cmake commands
@REM echo Building Open3D...
@REM cmake -DBUILD_WEBRTC=OFF -DBUILD_SHARED_LIBS=ON -G "Visual Studio 16 2019" -A x64 -DCMAKE_INSTALL_PREFIX="%targetDir%" -S . -B build
@REM if errorlevel 1 (
@REM     echo Failed to run cmake configuration command.
@REM     exit /b 1
@REM )

@REM cmake --build build --config Release --target ALL_BUILD
@REM if errorlevel 1 (
@REM     echo Failed to build ALL_BUILD.
@REM     exit /b 1
@REM )

@REM cmake --build build --config Release --target INSTALL
@REM if errorlevel 1 (
@REM     echo Failed to install.
@REM     exit /b 1
@REM )

@REM echo Done.
@REM endlocal