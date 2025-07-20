import os.path
from typing import Any, Union

from flask import render_template
from markupsafe import Markup
from fileMapping.core.helperFunctions import getAppRegister
# from fileMapping import appRegister, getAppRegister

from .config import path


# 这个是对 path 的相对路径做出适配
# 详情注释请看 /resources/static/pages/includes/.md

def _regis(name: str, **key) -> str:
    return render_template(path + name, **key)


class Commons:
    def __init__(self, path):
        # 这个是对 self.path 的相对路径做出适配
        # 详情注释请看 /resources/static/pages/includes/.md
        self.app = getAppRegister("fileFlask", "flaskApp")
        self.path = path

    def html(self, *args, **kwargs): ...

    def _regis(self, _TemplateName: str, **key) -> str:
        key = {
            # Markup 标记为安全 html 否则特殊字符会被替换
            key: Markup(data) for key, data in key.items()
        }
        with self.app.app_context():
            return render_template(os.path.join(self.path, _TemplateName + ".html").replace("\\", "/"), **key)


class Side(Commons):
    def __init__(self, path):
        super().__init__(path)

        self.name = "/side"
        self.single_li = self.Single_li(self.path + self.name)
        self.side_title = self.Side_title(self.path + self.name)
        self.multi_li = self.Multi_li(self.path + self.name, self.single_li)

    def html(self, title: str, ul: str, logo: str = "", **key) -> str:
        return self._regis("side", title=title, ul=ul, logo=logo, **key)

    class Multi_li(Commons):
        def __init__(self, path, single_li):
            super().__init__(path)

            self.multi_ti = self
            # 循环 Multi_li single_li
            self.single_li = single_li
            self.multi_title = self.Multi_title(self.path)

        def html(self, title: str, li: str, url: str = "#", icon: str = '', **key) -> str:
            return self._regis("multi_li", title=title, li=li, url=url, icon=icon, **key)

        class Multi_title(Commons):
            def html(self, title: str, i: Union[str, int] = '', **key) -> str:
                return self._regis("multi_title", title=title, i=i, **key)

    class Single_li(Commons):
        def html(self, title: str, url: str = "#", icon: str = '', **key) -> str:
            return self._regis("single_li", title=title, url=url, icon=icon, **key)

    class Side_title(Commons):
        def html(self, title: str) -> str:
            return self._regis("side_title", title=title)


class TopBar(Commons):
    def __init__(self, path: str):
        super().__init__(path)

        self.name = "/topBar"
        self.left = self.Left(self.path + self.name)
        self.right = self.Right(self.path + self.name)

    class Left(Commons):
        def __init__(self, path: str):
            super().__init__(path)

            self.li_title = self.Li_title(path)

        def html(self, li_title: str, **key) -> str:
            return self._regis("left", li_title=li_title, **key)

        class Li_title(Commons):
            def html(self, title: str, **key) -> str:
                return self._regis("li_title", title=title, **key)

    class Right(Commons):
        def __init__(self, path: str):
            super().__init__(path)

            self.search = self.Search(self.path)
            self.information = self.Information(self.path)
            self.notice = self.Notice(self.path)
            self.fullScreen = self.FullScreen(self.path)
            self.avatar = self.Avatar(self.path)

        def html(self, component: str, **key) -> str:
            return self._regis("right", component=component, **key)

        class Search(Commons):
            def html(self, url: str, **key) -> str:
                return self._regis("search", url=url, **key)

        class Information(Commons):
            def __init__(self, path: str):
                super().__init__(path)

                self.message = self.Message(self.path)

            def html(self, i: str, message: str, url: str, **key) -> str:
                return self._regis("information", i=i, message=message, url=url, **key)

            class Message(Commons):
                def html(self, url: str, png: str, name: str, informationSimplification: str, time: str, **key) -> str:
                    return self._regis("message", url=url, png=png, name=name,
                                       informationSimplification=informationSimplification, time=time, **key)

        class Notice(Commons):
            def __init__(self, path: str):
                super().__init__(path)

                self.message = self.Message(self.path)

            def html(self, url: str, i: str, component: str, **key):
                return self._regis("notice", url=url, i=i, component=component, **key)

            class Message(Commons):
                def html(self, url: str, png: str, name: str, informationSimplification: str, time: str, **key) -> str:
                    return self._regis("message", url=url, png=png, name=name,
                                       informationSimplification=informationSimplification, time=time, **key)

        class FullScreen(Commons):

            def html(self, **key):
                return self._regis("fullScreen", **key)

        class Avatar(Commons):
            def __init__(self, path: str):
                super().__init__(path)

                self.avatar_clo = self.Avatar_clo(self.path)

            def html(self, jpg: str, userName: str, briefIntroduction: str, timeOfRegistration: str, component: str,
                     set: str,
                     logout: str, **key):
                return self._regis("avatar", jpg=jpg, userName=userName, briefIntroduction=briefIntroduction,
                                   timeOfRegistration=timeOfRegistration, component=component, set=set, logout=logout,
                                   **key)

            class Avatar_clo(Commons):
                def html(self, url: str, name: str):
                    return self._regis("avatar_clo", url=url, name=name)

    def html(self, left: str, right: str, **key) -> str:
        return self._regis("topBar", left=left, right=right, **key)


class Subject(Commons):
    def __init__(self, path):
        super().__init__(path)

        self.name = "/subject"

    def html(self, name: str = "", home: str = "#", component: str = "", **key) -> str:
        return self._regis("subject", name=name, home=home, component=component, **key)


class TheBarIsLow(Commons):
    def __init__(self, path):
        super().__init__(path)

        self.name = "/theBarIsLow"

    def html(self, **key) -> str:
        return self._regis("theBarIsLow", **key)
