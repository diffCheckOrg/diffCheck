FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Install g++ and make
RUN powershell.exe -Command \
    choco install mingw -y ; \
    choco install make -y