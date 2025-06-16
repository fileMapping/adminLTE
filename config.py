import os

from fileMapping import File


path = "pages\\includes"


side = os.path.join(path, "side")
topBar = os.path.join(path, "topBar")
subject = os.path.join(path, "subject")
theBarIsLow = os.path.join(path, "theBarIsLow")

dataPath = File.public.get("config", {}).get("adminlteDATA", "adminlteDATA")

templates_path = "templates"
