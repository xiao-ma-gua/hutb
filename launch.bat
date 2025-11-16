:: @echo off 
:: 需要预装的软件：Visual Studio 2019：https://aka.ms/vs/14/release/vs_community.exe
:: 当前目录下需要的软件包括：
:: carla1, unreal
:: CMake, GnuWin32, 
:: dotnet, Python37

:: 解决命令行显示的中文乱码（添加支持utf-8功能）
chcp 65001 > nul

setlocal enabledelayedexpansion
    
make launch ARGS="--chrono" >launch.log