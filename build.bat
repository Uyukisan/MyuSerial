@REM MyuSerial打包程序
@echo off
chcp 65001
echo [开始打包程序]

set current_dir=%cd%
set resource_dir=%current_dir%\resources
set target_dir=%current_dir%\dist\MyuSerial
set target_resource_dir=%target_dir%\resources
set requirements_file=%current_dir%\requirements.txt
set virtual_env=%current_dir%serial_env

if EXIST "%virtual_env%" (
    echo 进入虚拟环境...
    call %virtual_env%\Scripts\activate.bat
) else (
    echo 是否创建虚拟环境？（y/n）
    set /p USE_VENV=
)

if "%USE_VENV%" == "y" (
    echo 开始创建虚拟环境...
    python -m venv serial_env
    echo ...虚拟环境创建完成: serial_env
    echo 进入虚拟环境...
    call %virtual_env%\Scripts\activate.bat
)

if EXIST "%requirements_file%" (
    echo 开始安装依赖...
    pip install -r %requirements_file%
    echo ...依赖安装完成
)

echo 开始编译程序...
pyinstaller -F -w -i %resource_dir%\serial.ico --name=MyuSerial .\main.py --clean
echo ...程序编译完成

if EXIST "%target_dir%" (
    echo 覆盖程序目录...
) else (
    echo 创建程序目录...
    md %target_dir%
)

if EXIST "%target_resource_dir%" (
    echo 覆盖资源目录...
) else (
    echo 创建资源目录...
    md %target_resource_dir%
)

if EXIST "%resource_dir%" (
    echo 开始拷贝资源文件...
    xcopy %resource_dir% %target_resource_dir% /s /e /y
    echo ...资源文件拷贝完成
)

echo 开始拷贝程序文件...
move /y %current_dir%\dist\* %target_dir%\
echo ...程序文件移动完成

if EXIST "%virtual_env%" (
    echo ...退出虚拟环境
    call %virtual_env%\Scripts\deactivate.bat
)

echo [程序打包完成]
echo 是否打开程序所在目录？（y/n）
set /p OPEN_DIR=
if "%OPEN_DIR%" == "y" (
    start explorer %target_dir%
)
echo Have a great day!