#!/usr/bin/env python3
"""Original 192px visual previews for Vellora creator packs v7/v8/v9.

Previews are accurate CATEGORY illustrations, not screenshots of the live
character. Changes apply to the actual skinned 3D avatar in the Godot creator.
"""
from __future__ import annotations
from io import BytesIO
import math
from PIL import Image, ImageDraw

SIZE = 192
SKIN = (217, 161, 133, 255)
SKIN_DARK = (156, 97, 86, 255)
CYAN = (101, 223, 250, 255)
DARK = (10, 30, 49, 255)
BLUE = (21, 67, 93, 255)

def _rgba(color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    if not color.startswith("#") or len(color) != 7:
        return (228, 207, 178, alpha)
    return tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) + (alpha,)

def preview(spec: dict) -> bytes:
    kind = str(spec.get("category", ""))
    style = str(spec.get("style", ""))
    color = _rgba(str(spec.get("color", "#bfeeff")))
    im = Image.new("RGBA", (SIZE, SIZE), DARK)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, 187, 187), radius=22, fill=BLUE, outline=(39, 137, 173, 255), width=3)
    d.ellipse((25, 25, 167, 167), fill=(17, 48, 68, 255), outline=(46, 131, 165, 255), width=2)

    if kind == "nose":
        shape = spec.get("shape", {})
        wide = float(shape.get("width", 0))
        proj = float(shape.get("projection", 0))
        lift = float(shape.get("lift", 0))
        width = 16 + 10 * wide
        bridge = 94 + 5 * proj
        d.ellipse((50, 27, 141, 173), fill=SKIN, outline=SKIN_DARK, width=3)
        d.line([(96, 62), (94, 105), (bridge, 118 + lift * 8)], fill=SKIN_DARK, width=5, joint="curve")
        d.arc((96-width, 115+lift*6, 96+width, 139+lift*6), 8, 170, fill=(111, 70, 66), width=5)
        d.ellipse((96-width, 127+lift*6, 96-width+4, 132+lift*6), fill=(100, 52, 49))
        d.ellipse((96+width-4, 127+lift*6, 96+width, 132+lift*6), fill=(100, 52, 49))
    elif kind == "mouth":
        shape = spec.get("shape", {})
        spread = 32 + 15 * float(shape.get("width", 0))
        full = 8 + 8 * float(shape.get("fullness", 0))
        d.ellipse((34, 29, 159, 170), fill=SKIN, outline=SKIN_DARK, width=3)
        d.line([(96-spread, 103), (85, 99-full), (96, 103), (107, 99-full), (96+spread, 103)], fill=(145, 46, 60), width=4, joint="curve")
        d.line([(96-spread, 103), (91, 107+full), (102, 107+full), (96+spread, 103)], fill=(158, 58, 74), width=5, joint="curve")
    elif kind in ("eyeshadow", "lashes", "blush", "lipstick"):
        d.ellipse((31, 22, 161, 171), fill=SKIN, outline=SKIN_DARK, width=3)
        d.arc((50, 64, 85, 96), 180, 355, fill=(65, 45, 47), width=4)
        d.arc((107, 64, 142, 96), 180, 355, fill=(65, 45, 47), width=4)
        if kind == "lipstick":
            d.ellipse((76, 126, 118, 143), fill=color)
            d.line((76, 135, 118, 135), fill=(113, 59, 67), width=2)
        elif kind == "blush":
            for x in (62, 130):
                d.ellipse((x-19, 109, x+19, 132), fill=color)
        else:
            for x in (67, 125):
                d.arc((x-21, 59, x+21, 95), 170, 350, fill=color, width=9 if kind == "eyeshadow" else 4)
                if kind == "lashes":
                    for i in (-13, 0, 13):
                        d.line((x+i, 76, x+i-4, 63), fill=color, width=3)
    elif kind == "face_tattoo":
        d.ellipse((30, 20, 161, 172), fill=SKIN, outline=SKIN_DARK, width=3)
        design = str(spec.get("id", ""))
        if "estrela" in design or "coroa" in design:
            n = 5
            vertices = [(130+18*math.cos(math.pi*i/n), 75+18*math.sin(math.pi*i/n)) for i in range(n*2)]
            d.polygon(vertices, fill=(43, 37, 49))
        else:
            d.arc((104, 65, 156, 124), 75, 330, fill=(43, 37, 49), width=6)
            d.line((115, 100, 135, 130), fill=(43, 37, 49), width=6)
    elif kind in ("earring_plus", "nose_piercing", "brow_piercing", "lip_piercing", "eyewear"):
        if kind == "earring_plus":
            # Profile silhouette and properly proportioned lobe jewelry.
            d.ellipse((44, 24, 140, 164), fill=SKIN, outline=SKIN_DARK, width=3)
            d.ellipse((126, 96, 155, 124), fill=SKIN, outline=SKIN_DARK, width=2)
            x, y, r = 151, 113, 12
            if style in ("hoop", "double", "cuff"):
                d.ellipse((x-r, y-r, x+r, y+r), outline=color, width=5)
                if style == "double":
                    d.ellipse((x-9, y+10, x+9, y+28), outline=color, width=3)
            elif style in ("drop", "cross", "bar"):
                d.ellipse((x-5, y-5, x+5, y+5), fill=color)
                d.line((x, y+4, x, y+36), fill=color, width=5)
                if style == "cross":
                    d.line((x-12, y+22, x+12, y+22), fill=color, width=4)
            else:
                d.ellipse((x-8, y-8, x+8, y+8), fill=color, outline=(252, 255, 255), width=2)
        else:
            d.ellipse((30, 22, 163, 169), fill=SKIN, outline=SKIN_DARK, width=3)
            if kind == "eyewear":
                for x in (54, 110):
                    d.rounded_rectangle((x-26, 69, x+26, 103), radius=9, outline=color, width=5)
                d.line((80, 84, 85, 84), fill=color, width=5)
            else:
                y = 92 if kind == "nose_piercing" else 66 if kind == "brow_piercing" else 128
                d.ellipse((116, y, 135, y+19), outline=color, width=5)
                d.ellipse((116, y+5, 122, y+11), fill=(255, 255, 255))
    else:
        d.ellipse((62, 61, 130, 130), outline=CYAN, width=7)
    buf = BytesIO()
    im.save(buf, format="PNG", optimize=True, compress_level=9)
    return buf.getvalue()
