"""

adminLTE 的异常类
"""
from typing import Union, List

# from fileMapping.information import error
from fileMapping import abnormal

class File(abnormal.Mistake):
    def __init__(self, fileName: str, error: Exception, traceback: str):
        """
        这是一个 file 异常
        """
        self.file: str = fileName
        self.error = error
        self.traceback = traceback
        self.listOfLanguages = [
            self.english, self.chinese
        ]

    def english(self) -> str:
        return f"The file is abnormal: {self.file} error: {self.error}"

    def chinese(self) -> str:
        return f"文件异常: {self.file} error: {self.error}"


class Fileread(File):
    def english(self) -> str:
        return f"An exception occurred while the file was opened FILE: {self.file} error: {self.error}"

    def chinese(self) -> str:
        return f"文件在打开时发生异常 文件: {self.file} error: {self.error}"


class Template(abnormal.Mistake):
    def __init__(self): ...


class HowItWasGenerated(Template):
    def english(self) -> str: ...

    def chinese(self) -> str: ...


class TheWayIsMissing(HowItWasGenerated):
    def __init__(self, file: str, howItWasGenerated: list):
        # 这个没有用了
        self.file = file
        self.wayList = howItWasGenerated
        self.listOfLanguages = [
            self.english, self.chinese
        ]

    def english(self) -> str:
        return f"There is no way to spawn or there is a wrong way to spawn FILE: {self.file}"

    def chinese(self) -> str:
        return f"没有任何的生成方式可以生成或者生成方式有错误 文件: {self.file}"


class Attribute(Template):
    def __init__(self, missingAttributes: str, attributes: List[str]):
        self.missingAttributes = missingAttributes
        self.attributes = [i for i in attributes if not (i.startswith("__") or i == 'html')]
        self.listOfLanguages = [
            self.english, self.chinese
        ]

    def english(self) -> str:
        return f"Template exceptions/errors occur in multi-structure builds, missing attributes Attribute: {self.missingAttributes}"

    def chinese(self) -> str:
        return f"模板在多结构的生成中发生异常/错误缺少属性 属性: {self.missingAttributes}"


class Notemplates(Template):
    def __init__(self, template):
        # 没有这个模板 error
        self.template: str = template
        self.listOfLanguages = [
            self.english, self.chinese
        ]

    def english(self):
        return f"This template is not available in Major If you're sure you have this {self.template} template Please " \
               f"check that adminLTE.templates.Mainly is currently using the following template: {self.template}"

    def chinese(self):
        return f"没有 Mainly 这个模板 如果你确定有这个 {self.template} 模板 请检查一下 adminLTE.templates.Mainly 当前使用的模板是: {self.template}"


class Specification(Template):
    def __init__(self, key):
        self.key: str = key
        self.listOfLanguages = [
            self.english, self.chinese
        ]

    def english(self):
        return f"Missing key: {self.key}"

    def chinese(self):
        return f"缺少键: {self.key}"


class TemplateTypeError(Template):
    def __init__(self, type, typeShouldBe: Union[list, tuple]):
        self.type = type
        self.typeShouldBe = typeShouldBe
        self.listOfLanguages = [
            self.english, self.chinese
        ]

    def english(self):
        return f"Type-wrong shouldn't be: {self.type} It should be: {self.typeShouldBe}"

    def chinese(self):
        return f"类型错误 不应该是: {self.type} 应该为: {self.typeShouldBe}"


template_error_all = (Template, HowItWasGenerated, TemplateTypeError,
                      Attribute, Notemplates, Specification, TemplateTypeError)
