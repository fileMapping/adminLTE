from flask import render_template

from .config import path


# 这个是对 path 的相对路径做出适配
# 详情注释请看 /resources/static/pages/includes/.md


def _regis(name: str, **key) -> str:
    return render_template(path + name, **key)


def side(title: str = "", ul: str = "", logo: str = "", **key) -> str:
    return _regis("side.html", title=title, ul=ul, logo=logo, **key)


def topBar(left: str, right: str, **key) -> str:
    return _regis("topBar.html", left=left, right=right, **key)


def subject(name: str = "", home: str = "#", component: str = "", **key) -> str:
    return _regis("subject.html", name=name, home=home, component=component, **key)


def theBarIsLow(**key) -> str:
    return _regis("theBarIsLow.html", **key)
