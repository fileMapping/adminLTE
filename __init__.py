"""
这个插件是AdminLTE的模板

templates.py 是对AdminLTE的骨架适配
"""
import os

from fileMapping import method

from . import generators
from . import templates
from . import config
from . import init


__dataFolders__ = [config.dataPath]


def main():
    path = method.dataFolders(config.dataPath)

    if os.listdir(path).__len__() == 0:
        # 创建初始化
        init.init(config.templates_path)

