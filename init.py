# 这个一般是 adminLTE 插件第一次运行时的 init
import json
import os

from fileMapping import File, method

from . import config


def init(templates_path):
    path = method.dataFolders(config.dataPath)  # 获取 data 文件夹
    templates_path = os.path.join(path, templates_path)
    _mkdir(templates_path)
    createAFile(templates_path, fileTree)
    createAProfile(path)


def createAProfile(file_path):
    # 创建配置文件
    _open(os.path.join(file_path, "config.json"), {
        "懒得写了": "以后再说"
    })


def createAFile(path: str, file_data: dict):
    """
    这个函数是一个根据 dict 数据生成文件树
    :param path:
    :param file_data:
    :return:
    """

    def _(path, file_data: dict):
        # 递归创建
        for key, data in file_data.items():
            filePath = os.path.join(path, key)
            if isinstance(data, dict) and (key.find('.') == -1):
                _mkdir(filePath)
                _(filePath, data)

            else:
                _open(filePath, data)

    _(path, file_data)


def _open(path: str, data: str | dict) -> bool:
    try:
        with open(path, mode='w', encoding='utf-8') as f:
            if isinstance(data, dict):
                json.dump(data, f, ensure_ascii=False, indent=4)

            else:
                f.write(data)

        return True
    except Exception as e:
        File.callObject.adminLTE.logs["open"] = {
            "path": path,
            "data": data,
            "e": e
        }
        return False


def _mkdir(path: str) -> bool:
    # 创建一个文件夹
    try:
        os.mkdir(path)
        return True

    except Exception as e:
        # 日志
        File.callObject.adminLTE.logs["mkdir"] = {
            "path": path,
            "e": e
        }
        return False


side = {
    # 测试
    "logo": "",
    "title": "屌爆了",
    "ul": [

    ]
}

topBar = {
    "left": {},
    "right": {}
}

subject = {

}

fileTree = {
    "side": {
        "example.json": side,
    },
    "topBar": {
        "example.json": topBar,
    },
    "subject": {
        "example.json": subject,
    },
    "theBarIsLow": {
        "example.json": {},
    }
}


"""
由于字典的键唯一性
现将部分 部分生成方法改为 当遇到列表时 其中元素必须是字典 必须包含这两个值 type parameters

[
    "type": "<component>",
    "parameters": {
        ...
    }
]
"""