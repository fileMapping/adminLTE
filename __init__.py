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


def main(fileMapping: File):
    path = helperFunctions.getAppRegister("Folders", "getTemporaryFolders")
    path = path(__dataFolders__[0])

    if os.listdir(path).__len__() == 0:
        # 创建初始化
        init.init(config.templates_path)

    templates.mainly = templates.Mainly(fileMapping.plugInRunData.pluginConfig["adminLTE"]["path"])
    # 这个地方需要修改，需要传入插件的配置


__dataFolders__ = [config.dataPath]

__init__ = main



