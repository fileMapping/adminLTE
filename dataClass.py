from typing import Optional
from typing import Generic, TypeVar

from . import abnormal

DictOfData_T = TypeVar("DictOfData_T", bound="DictOfData")


class d1(dict):
    type: str
    parameters: dict


class ListOfData(list, Generic[DictOfData_T]): ...


class DictOfData(dict):
    type: str
    parameters: dict | d1 | ListOfData

    def __init__(self, type: str, parameters: dict):
        super().__init__()

        self.type: str = type
        self.parameters: dict | d1 | ListOfData = parameters

    def check(self) -> bool:
        # 检查 data 是否包含 ["type", "parameters"]
        l = [
            i for i in ["type", "parameters"] if not (i in [self])
        ]
        return True if len(l) == 0 else abnormal.Specification(' | '.join(l))
