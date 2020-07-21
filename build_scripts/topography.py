import json
import os
import subprocess

from PIL import Image, ImageDraw

try:
    from palette import parse_palette
except ImportError:
    from build_scripts.palette import parse_palette


dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.realpath(os.path.join(dir_path, '..'))
topo_path = os.path.join(project_path, "topography")
topo_source = os.path.join(project_path, "cst_out_new", "CDDATA.CXT", "Standalone")

palette, palette_index, colors, component_colors = parse_palette(os.path.join(dir_path, 'grayscale.pal'))

if not os.path.exists(topo_path):
    os.mkdir(topo_path)

metadata = json.load(open(os.path.join(topo_source, "..", "metadata.json")))
for num in range(693, 748 + 1, 2):
    data = metadata["libraries"][0]["members"][str(num)]
    data2 = metadata["libraries"][0]["members"][str(num + 1)]
    if data["name"] != data2["name"][:-2]:
        raise ValueError("Name mismatch")

    with open(os.path.join(topo_source, str(num) + ".txt"), "rb") as fp:
        data_string = fp.read()
    with open(os.path.join(topo_source, str(num + 1) + ".txt"), "rb") as fp:
        data_string += fp.read()

    im = Image.new("P", [316, 198])
    im.putpalette(palette)

    draw = ImageDraw.Draw(im)
    draw.rectangle([(0, 0), (315, 197)], 0xF0)

    y = 0
    x = 0
    for byte in data_string:
        draw.point([x, y], byte)

        x += 1
        if x >= 316:
            y += 1
            x = 0

    im.save(os.path.join(topo_path, data["name"] + ".png"))

project_file = os.path.join(dir_path, 'topography.ftpp')
subprocess.call(['npx', 'free-tex-packer-cli', '--project', project_file, '--output', topo_path])
