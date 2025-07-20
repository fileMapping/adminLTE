"""
这个插件是AdminLTE的模板

是对AdminLTE的骨架适配

可以使用 json 生成 AdminLTE 的html代码
"""
import os

from fileMapping import helperFunctions
from fileMapping import File

from . import generators
from . import templates
from . import config
from . import init


def main():
    path = helperFunctions.getAppRegister("Folder", "getTemporaryFolders")
    path = path(__dataFolders__[0])

    if os.listdir(path).__len__() == 0:
        # 创建初始化
        init.init(config.templates_path)


__dataFolders__ = [config.dataPath]

__init__ = main



