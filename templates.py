import os

import rich

from . import config
# config

# from . import mainly
from . import component


# 这个是对 path 的相对路径做出适配
# 我对模板分为2类
# mainly.py
# component.py


# @appRegister("GeneratorsMainly")
class Mainly(component.Commons):
    def __init__(self, path: str):
        super().__init__(path)

        self.side: component.Side = component.Side(path)
        self.topBar: component.TopBar = component.TopBar(path)
        self.subject: component.Subject = component.Subject(path)
        self.theBarIsLow: component.TheBarIsLow = component.TheBarIsLow(path)

        l = {
            "side": self.side,
            "topBar": self.topBar,
            "subject": self.subject,
            "theBarIsLow": self.theBarIsLow
        }
        self.index = self.Index(os.path.dirname(path), l)

    class Index(component.Commons):
        def __init__(self, path, l):
            super().__init__(path)

            self._add(l)

        def _add(self, l: dict):
            for name, dj in l.items():
                exec(f"self.{name} = dj")

        def html(self, side, topBar, subject, theBarIsLow, *args, **kwargs):
            return self._regis("index", side=side, topBar=topBar, subject=subject, theBarIsLow=theBarIsLow)


mainly: Mainly | component.Side | component.TopBar | \
        component.Subject | component.TheBarIsLow = Mainly(config.path)
