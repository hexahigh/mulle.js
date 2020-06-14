import os
from shutil import copy

dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.realpath(os.path.join(dir_path, '..'))
ui_source = os.path.join(project_path, "cst_out_new", "00.CXT", "Standalone")
arrows_source = os.path.join(project_path, "cst_out_new", "05.DXR", "Internal")
ui_path = os.path.join(project_path, "dist", "ui")

data_source = os.path.join(project_path, "data")
data_path = os.path.join(project_path, "dist", "data")

if not os.path.exists(ui_path):
    os.mkdir(ui_path)

if not os.path.exists(data_path):
    os.mkdir(data_path)


def copy_ui(source, dest):
    copy(
        os.path.join(ui_source, str(source) + ".png"),
        os.path.join(ui_path, str(dest) + ".png"),
    )


copy_ui(109, "default")
copy_ui(110, "grab")
copy_ui(111, "left")
copy_ui(112, "point")
copy_ui(113, "back")
copy_ui(114, "right")
copy_ui(115, "drag_left")
copy_ui(116, "drag_right")
copy_ui(117, "drag_forward")

for num in range(161, 192):
    source_file = os.path.join(arrows_source, str(num) + ".png")
    dest_file = os.path.join(ui_path, str(num) + ".png")
    copy(source_file, dest_file)

copy(os.path.join(project_path, "loading.png"), os.path.join(project_path, "dist"))

for file in os.scandir(os.path.join(data_source)):
    copy(file, os.path.join(project_path, "dist", "data"))
