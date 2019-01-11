from cx_Freeze import setup, Executable
import sys
import os

# 增加
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
print('PYTHON_INSTALL_DIR', PYTHON_INSTALL_DIR)
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


# 主程序手动命名
target_name = 'mcasertool.exe'

build_exe_options = {
    "include_files": ["logo.ico", "README.MD", "LICENSE",
                      os.path.join(PYTHON_INSTALL_DIR, 'Scripts', 'tk86t.dll'),
                      os.path.join(PYTHON_INSTALL_DIR, 'Scripts', 'tcl86t.dll')
                      ],
    # 包含外围的ini、jpg文件，以及data目录下所有文件，以上所有的文件路径都是相对于cxsetup.py的路径。
    "packages": ["mca_sertool"],  # 包含用到的包
    "includes": [],
    "excludes": ["unittest"],  # 提出wx里tkinter包
    "path": sys.path,  # 指定上述的寻找路径
    #  "icon": "COMToolData/assets/logo.ico"                        #指定ico文件
}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# 简易方式定义快捷方式，放到Executeable()里。
# shortcutName = "AppName",
# shortcutDir = "ProgramMenuFolder"
setup(name="mca_sertool",
      author="zozo",
      version="0.1.0",
      description="zozo's first project with tkinter",
      options={"build_exe": build_exe_options},
      executables=[Executable("mca_sertool/mainwindow.py",
                              targetName=target_name,
                              base=base,
                              icon=r"logo.ico")
                   ])
