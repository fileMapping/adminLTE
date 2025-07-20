import os
import json
import traceback
import types
from typing import Dict, Any, Union, List


# from fileMapping import File, method
from fileMapping.core import decorators
from fileMapping.core import helperFunctions
# from fileMapping import appRegister

# from . import mainly
from . import templates
from . import config
from . import abnormal
from . import dataClass


app = decorators.tagAppRegistration(config.__name__)


@app()
def specificTemplates(path: str, templatePath: str = None) \
        -> Union[str, abnormal.Fileread, abnormal.Attribute, abnormal.TheWayIsMissing]:
    """
    加载一个特定模板
    json -> dict -> html
    模板读取 相对路径 {file_DATA}/adminlteDATA/templates
    :param templatePath:
    :param generate_manner: 加载 yellow
    :param path: 文件路径
    :return:
    """
    file_data = templateRead(path)
    if isinstance(file_data, abnormal.Fileread):
        return file_data

    file_data = templateLoader(file_data)
    if isinstance(file_data, abnormal.Attribute):
        return file_data

    html = multipleStructures(file_data, path=templatePath)
    if isinstance(html, abnormal.Attribute):
        return html

    return html


@app()
def multipleStructures(data: Union[dict, list], path: str = None) -> Union[
    str, abnormal.Attribute, abnormal.Specification]:
    """
    多结构生成
    dict -> html

    :param data:
    :param path:
    # :param generate_manner: 生成方式
    :return: html
    """
    wayList = [
        i for i in dir(templates.Mainly) if not i.startswith("_")
    ]

    def specification(data: dict) -> Union[bool, abnormal.Specification]:
        # 检查 data 是否包含 ["type", "parameters"]
        l = [
            i for i in ["type", "parameters"] if not (i in data)
        ]
        return True if len(l) == 0 else abnormal.Specification(' | '.join(l))

    def listProcessing(generate_manner: templates.Mainly,
                       data: List[Union[dataClass.ListOfData, dict]]) \
            -> Union[str, abnormal.Attribute, abnormal.Specification, abnormal.TemplateTypeError, abnormal.Notemplates]:
        ju = []
        for i in data:
            # 检查
            check = specification(i)
            if isinstance(check, abnormal.template_error_all):
                return check

            # dictionaryProcessing 生成 html
            htmlData = dictionaryProcessing(generate_manner, i)
            if isinstance(htmlData, abnormal.template_error_all):
                return htmlData

            ju.append(htmlData)

        return '\n'.join(ju)

    def dictionaryProcessing(generate_manner: templates.Mainly,
                             data: Union[
                                 dataClass.DictOfData, dict]) -> Union[
        str, abnormal.Attribute, abnormal.TemplateTypeError, abnormal.Notemplates]:
        ju = {}
        for key, value in data["parameters"].items():
            if isinstance(value, list):
                if not data["type"] in dir(generate_manner):
                    return abnormal.Attribute(data["type"], dir(generate_manner))

                dp = getattr(generate_manner, data["type"])
                value = listProcessing(dp, value)
                if isinstance(value, abnormal.template_error_all):
                    # 错误 Template
                    return value

            elif isinstance(value, dict):
                dp = getattr(generate_manner, data["type"])
                value = dictionaryProcessing(dp, value)
                if isinstance(value, abnormal.template_error_all):
                    # 错误 Template
                    return value

            elif isinstance(value, (str, int, float)):
                pass

            else:
                return abnormal.TemplateTypeError(type(value), (list, str, int))

            ju[key] = value
        # 生成 html
        keyType: str = data["type"].replace("//", "/").replace("\\", "/")
        if keyType.find("/") == -1:
            # 相对引用
            if not keyType in dir(generate_manner):
                return abnormal.Attribute(keyType, dir(generate_manner))

            return getattr(generate_manner, keyType).html(**ju)

        else:
            # 绝对引用
            # 用不到 generate_manner
            lit = keyType.split("/")
            if lit[0] in wayList:
                # 确定模板没有错误
                return abnormal.Notemplates(lit[0])

            _ = templates.Mainly(generate_manner.path)
            for i in lit:
                if not i in dir(_):
                    return abnormal.Attribute(i, dir(_))
                _ = getattr(_, i)

            return _.html(**ju)

    mainly = templates.mainly if path == None else templates.Mainly(path)
    # 请不要简写 if 的判断
    if isinstance(data, dict):
        check = specification(data)
        if check != True:
            return check
        return dictionaryProcessing(mainly, data)

    elif isinstance(data, list):
        return listProcessing(mainly, data)


@app()
def templateLoader(data: dict) -> Union[dict, abnormal.Fileread]:
    """
    {file_DATA}/adminlteDATA/templates
    此加载器 会将一个文件夹内需要调用的一个文件夹进行调用
    只会简单的判断"{{0}}"请不要恶意编写 会递归加载 不要编写 依赖循环的模板
    如:
        templates/a.json
        {
            "logo": "",
            "title": "屌爆了",
            "ul": "{{ b.json }}"
        }
        templates/a.json
        {
            "left": {},
            "right": {}
        }
        当加载了 a.json 之后
        {
            "logo": "",
            "title": "屌爆了",
            "ul": {
                "left": {},
                "right": {}
            }
        }
    :param data:
    :return:
    """

    def file_dict_recursion(data: dict) -> dict:
        _ = {}
        for key, data in data.items():
            if isinstance(data, dict):
                _[key] = file_dict_recursion(data)

            elif isinstance(data, (str, int)):
                data = str(data)
                if not (data.startswith("{{") and data.endswith("}}")):
                    _[key] = data
                    continue
                file_name = data.replace(" ", '').split("{{")[-1].split("}}")[0]
                file_data = templateRead(file_name)
                if isinstance(file_data, abnormal.Fileread):
                    # 无法打开文件 or 文件异常
                    raise file_data

                _[key] = file_dict_recursion(file_data)

            else:  # list
                _[key] = [
                    file_dict_recursion(i) for i in data
                ]

        return _

    try:
        return file_dict_recursion(data)

    except abnormal.Fileread as e:

        File.logs.plugInsOutput(e)
        return e


def templateRead(path: str) -> Union[dict, abnormal.Fileread]:
    """
    文件路径
    模板读取 相对路径 {file_DATA}/adminlteDATA/templates
    :param path:
    :return:
    """
    getTemporaryFolders = helperFunctions.getAppRegister("Folders", "getTemporaryFolders")
    if getTemporaryFolders == None:
        return

    path = os.path.join(getTemporaryFolders("templates"), path)
    # path = os.path.join(method.dataFolders(config.dataPath), "templates", path)
    if os.path.isfile(path):
        return _open(path)


def _open(path: str) -> Union[dict, abnormal.Fileread]:
    try:
        with open(path.replace('/', "\\"), mode='r', encoding='utf-8') as f:
            return json.load(f)

    except Exception as e:
        return abnormal.Fileread(path, e, traceback.format_exc())


getTemporaryFolders = helperFunctions.getAppRegister("Folders", "getTemporaryFolders")
rich.inspect(getTemporaryFolders)