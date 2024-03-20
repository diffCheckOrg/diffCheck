FROM mcr.microsoft.com/windows/servercore:ltsc2019

# install cmake
RUN powershell -Command \
    $ErrorActionPreference = 'Stop'; \
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest $('

# COnfig the environment
RUN setx /M PATH "%PATH%;C:\Program Files\mingw-w64\x86_64-8.1.0-win32-seh-rt_v6-rev0\mingw64\bin"

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run g++ to compile the code
CMD [ "g++", "main.cpp", "-o", "main.exe" ]
```
