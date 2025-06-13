:: @echo off
setlocal enabledelayedexpansion

:: =============================================
:: 配置区域（可根据需求修改）
:: =============================================
:: 需要创建虚拟环境的Python版本列表（格式：x.y，如3.7、3.11）
set PYTHON_VERSIONS="3.7 3.8 3.9 3.10 3.11"

:: 虚拟环境的根目录（所有版本的虚拟环境将存放在此目录下的子文件夹中）
set VENV_ROOT="C:\software\anaconda3\envs\"


chcp 65001

set http_proxy=http://127.0.0.1:7890
set https_proxy=http://127.0.0.1:7890

:: python.exe
set PATH=C:\software\anaconda3;%PATH%

:: where.exe
set make_path="C:\Windows\System32"
set PATH=%make_path%;%PATH%

:: make.exe
set make_path="C:\software\GnuWin32\bin"
set PATH=%make_path%;%PATH%

:: python 2.7, 3.7-3.14
:: conda create -n hutb_3.8 python=3.8
:: conda activate hutb_3.8
:: 
:: 删除已编译好的 boost 库
:: 删除所有文件 (删不了目录)
:: del Build\boost-1.80.0-install\* /q /f /s
:: 删除所有目录
:: rd /s /q Build\boost-1.80.0-install
:: 
:: make PythonAPI
:: conda deactivate

:: 遍历每个 Python 版本，创建虚拟环境
for %%v in (%PYTHON_VERSIONS%) do (
    :: 定义当前版本的虚拟环境路径
    set VENV_DIR=%VENV_ROOT%\py%%v
    echo %VENV_DIR%
)

%WINDIR%\System32\cmd.exe "/K" C:\software\anaconda3\Scripts\activate.bat C:\software\anaconda3\envs\carla_dev
:: conda activate carla_dev


:: vs 2019
%comspec% /k "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"

call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"



cd C:\ProgramData\Jenkins\.jenkins\workspace\carla
