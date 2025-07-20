import os

from fileMapping import File


path = "pages\\includes"


side = os.path.join(path, "side")
topBar = os.path.join(path, "topBar")
subject = os.path.join(path, "subject")
theBarIsLow = os.path.join(path, "theBarIsLow")

dataPath = "adminlteDATA"

templates_path = "templates"
# templates_path 在dataPath下 所以这里的路径应该是"adminlteDATA\\templates"


__name__ = "AdminLTE"
__version__ = "1.0.0"

