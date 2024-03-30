#!/bin/sh
echo "[开始打包程序]"
current_dir=$(pwd)
resource_dir="${current_dir}/resources"
requirements_file="${current_dir}/requirements.txt"
virtual_env="${current_dir}/serial_env"
python_bin="$(which python || which python3 || echo nopython)"
target_dir="${current_dir}/dist"

if [ $python_bin == "nopython" ];then
    echo "未检测到python，请先安装python: https://www.python.org"
    echo "Have a great day!"
    exit
fi
if [ ! -d $virtual_env ];then
    echo "是否创建虚拟环境？(y/n)"
    read USE_VENV
else
    echo "进入虚拟环境..."
    source "${virtual_env}/bin/activate"
fi

if [ $USE_VENV == "y" ];then
    echo "开始创建虚拟环境..."
    $python_bin -m venv serial_env
    echo "...虚拟环境创建完成:serial_env"
    source "${virtual_env}/bin/activate"
fi

if [ -f $requirements_file ];then
    echo "开始安装依赖..."
    pip install -r $requirements_file
    echo "...依赖安装完成"
fi

echo 开始编译程序...
pyinstaller -F -w -i "${resource_dir}/serial.icns" --name=MyuSerial --add-data="resources:resources" ./main.py --clean
echo ...程序编译完成

if [ -d $virtual_env ];then
    echo "...退出虚拟环境"
    deactivate
fi

echo "[程序打包完成]"
echo "程序所在: ${target_dir}"
echo "Have a great day!"