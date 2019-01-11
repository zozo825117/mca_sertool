mca_sertool
===========

[![PyPi](https://img.shields.io/pypi/v/mca_sertool.svg)](https://pypi.python.org/pypi/mca_sertool)

> zozo's first project with tkinter

A cross platform serial debug tools written by python
--------
基于tkinter的串口解析工具，通过设置包的格式，自动对接受数据进行解析，并分类存储。

# Usage


- [x] cross platform (Windows, Linux, MacOS, Raspberry Pi ... ...)
- [x] tkinter
- [x] tkinter 全局缩放
- [x] tkinter 右键菜单
- [x] port baudrate bytesize parity stopbits settings
- [x] basic send data (ascii and hex)
- [x] basic receive data (ascii and hex)
- [x] send and receive data count
- [x] clear received data area
- [x] auto linefeed on every once receive
- [x] scheduled auto send
- [x] send history and select send again
- [x] serial auto detect
- [x] CR LF / LF select support
- [x] 正则表达式解析
- [x] log打印
- [x] build exe

# TODO

- [ ] HEX数据无法添加标签
- [ ] 生成ID速度问题
- [ ] ID校验格式
- [ ] json格式描述
- [ ] MQTT连接
- [ ] 文件保存
- [ ] 数据库支持

# Installation

## Windows

Test pass on Win10

there's three ways:
1. download excutable bin file, easiest way for one never used python
  * Download the latest bin file at the [release page](https://github.com/Neutree/COMTool/releases)
  * unzip, and run comtool.exe
2. Install Python3 first then install from pypi:
  * [dowload python3](https://www.python.org/downloads/)
  * Install by pip,
```
pip install comtool
comtool
```
3. Or you can download source code, then install from source code
  * download sourcecode
  * install
```
python setup.py bdist_wheel
pip install dist/COMTool-*.*.*-py3-none-any.whl
comtool
```


# Requirements

见 requirements.txt

# Development


1. Install python3.6 and pip3

Windows: 
  [dowload python3](https://www.python.org/downloads/)
  
2. Install virtualenv and virtualenvwrapper

Windows: 
  * [virtualenv安装](https://www.jianshu.com/p/a22cfdcc2558)
  * 生成虚拟环境 mca_sertool_env  `use Windows Powershell` 

```
cd E:\virtual_envs_works\
virtualenv -p "D:\Program Files\Python\Python36\python.exe" mca_sertool_env
```

2. install requirements.txt
```
pip install -r requirements.txt
```
检查安装情况：
```
pip list
```

```
Package    Version
---------- -------
cx-Freeze  5.1.1
pip        18.1
pyserial   3.4
setuptools 40.0.0
wheel      0.32.3

```


3. clone project

仓库地址：
[mca_sertool](http://www.zozo825117.cn:60010/summary/python%2Fmca_sertool.git) or
```
git clone http://<user name>@www.zozo825117.cn:60010/r/python/mca_sertool.git
```

4. code, resolve bugs or add new reatures

    Recommended `PyCharm` IDE to get start


5. pull request

# Build
1. 你需要从python3.6环境中手动复制以下文件
    `tk86t.dll
    tcl86t.dll`
    到这个路径下：
    `E:xxx\mca_sertool_env\Scripts\`

2. 用 `cxsetup.py`脚本构建可执行文件，生成的exe文件包可独立运行，并且支持多开。
    
    在工程文件夹下,shift+右键打开 `powershell` or `cmd命令控制符`也是一样支持的，并且cmd中workon可以直接使用
```
cmd /k workon mca_sertool_env # 进入虚拟环境
python cxsetup.py build # 在build路径下生成执行文件包
```


# References
[COMTool](https://github.com/Neutree/COMTool)

[![PyPI](https://img.shields.io/pypi/v/comtool.svg)](https://pypi.python.org/pypi/comtool/)

# Licence

The code is available at [GitHub][home] under the [MIT license][license].

# Authors

`mca_sertool` was written by `zozo <zjh@lierda.com>`

[home]: https://github.com/revolunet/sublimetext-markdown-preview
[license]: http://revolunet.mit-license.org

