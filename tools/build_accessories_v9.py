#!/usr/bin/env python3
"""Vellora v9 - original low-poly skinned-rig jewelry and eyewear profiles."""
import argparse
import json
import zipfile
import hashlib
from pathlib import Path
from appearance_previews import preview

# category, 8-10 choices (slug, label, 3D style, color, scale).
PACK = {
    "earring_plus": [
        ("ponto_lux","Ponto de luz premium","stud","#e8d5b0",1.0),
        ("argola_slim","Argola fina","hoop","#e4e7ed",.9),
        ("argola_gold","Argola dourada","hoop","#e5bd58",1.18),
        ("argola_dupla","Argola dupla","double","#e4e7ed",1.0),
        ("diamante","Diamante lapidado","gem","#a5e0fc",1.0),
        ("cristal","Cristal lilás","gem","#b894e0",1.14),
        ("pendente","Pendente longo","drop","#dfc58c",1.0),
        ("barra","Brinco industrial","bar","#c2d2d9",1.10),
        ("cruz","Cruz pendente","cross","#dadee8",1.0),
        ("ear_cuff","Ear cuff triplo","cuff","#d8b6a2",1.0)
    ],
    "nose_piercing": [
        ("stud_left","Pedrinha esquerda","left_stud","#ebd6a5",.95),
        ("stud_right","Pedrinha direita","right_stud","#cce8ef",.95),
        ("stud_double","Piercing duplo","double_stud","#b6d1f8",.9),
        ("hoop_left","Argola lateral esquerda","left_hoop","#e3ba63",.95),
        ("hoop_right","Argola lateral direita","right_hoop","#dce5ed",.95),
        ("septum","Septum fino","septum","#e0bb78",1.0),
        ("septum_gold","Septum dourado","septum","#e5b65c",1.19),
        ("septum_double","Septum duplo","septum_double","#d5d8e0",1.0)
    ],
    "brow_piercing": [
        ("bar_left","Sobrancelha esquerda","left_bar","#c6d5e2",1.0),
        ("bar_right","Sobrancelha direita","right_bar","#e1b970",1.0),
        ("hoop_left","Argola na sobrancelha E","left_hoop","#dddbe4",1.0),
        ("hoop_right","Argola na sobrancelha D","right_hoop","#d0b2bc",1.0),
        ("double_left","Piercing duplo esquerdo","double_left","#cfdeed",1.0),
        ("double_right","Piercing duplo direito","double_right","#e3be76",1.0),
        ("crystal","Cristal na sobrancelha","crystal","#88d6e0",1.05),
        ("bridge","Bridge metálico","bridge","#dddfe5",1.0)
    ],
    "lip_piercing": [
        ("labret","Labret central","labret","#d9dfe9",1.0),
        ("labret_gold","Labret dourado","labret","#e2b467",1.18),
        ("monroe","Monroe","monroe","#cfe7ff",1.0),
        ("medusa","Medusa","medusa","#e0bfd0",1.0),
        ("snake_bites","Snake bites","snake_bites","#d8dce5",1.0),
        ("spider_bites","Spider bites","spider_bites","#e2bd74",1.0),
        ("lower_hoop","Argola no lábio","lower_hoop","#dbe1e9",1.0),
        ("double_hoop","Argolas duplas","double_hoop","#d6b7c2",1.0)
    ],
    "eyewear": [
        ("aviator_gold","Aviador dourado","aviator","#e5b96d",1.0),
        ("aviator_silver","Aviador prateado","aviator","#d1e0e7",1.0),
        ("round_black","Redondo preto","round","#242b37",.93),
        ("round_gold","Redondo dourado","round","#e4b968",.93),
        ("sport","Óculos esportivo","sport","#3b7089",1.03),
        ("square","Quadrado moderno","square","#242e3d",1.0),
        ("cat_eye","Gatinho elegante","cat","#683d55",1.0),
        ("sun_shades","Óculos de sol","sun","#252634",1.08)
    ]
}

# All published v9 preset IDs remain stable; these are additional colors,
# scales and silhouettes produced by the same 3D renderer attached to Head.
PACK["earring_plus"] += [
    ("mini_huggie","Argola pequena","hoop","#ddeaf2",.75),
    ("pearl","Pérola natural","gem","#fff3e0",.78),
    ("obsidian","Pedrinha preta","stud","#253142",.83),
    ("gold_drop","Gota dourada","drop","#d8b45f",.86),
    ("ice_double","Argolas gelo","double","#9eefff",.90),
    ("rose_cuff","Ear cuff rosé","cuff","#dbacaa",.80),
]
PACK["nose_piercing"] += [
    ("mini_gold","Ponto de ouro","left_stud","#dbb25d",.72),
    ("septum_silver","Septum prateado","septum","#dde9ef",.78),
]
PACK["brow_piercing"] += [
    ("rose_bar","Barra rosé","left_bar","#cc9698",.77),
    ("thin_hoop","Argola delicada","right_hoop","#e1e7ef",.78),
]
PACK["lip_piercing"] += [
    ("mini_labret","Labret discreto","labret","#c3e6f0",.78),
    ("gold_hoop","Argola dourada","lower_hoop","#e3bc6b",.88),
]
PACK["eyewear"] += [
    ("steel_aviator","Aviador aço","aviator","#bad2df",.90),
    ("retro_square","Quadrado retrô","square","#885a67",.89),
]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out", default="Vellora-Ara-Accessories-v9.zip")
    output=Path(parser.parse_args().out)
    presets=[]
    for category, variants in PACK.items():
        for slug,label,style,color,scale in variants:
            assert 0.7 <= scale <= 1.4 and len(label) <= 48
            presets.append({"id":f"v9_{category}_{slug}", "category":category,
                            "label":label, "style":style,"color":color, "scale":scale})
    assert len(presets)==56 and len({item["id"] for item in presets})==56
    thumbnails={}
    for item in presets:
        fname=f"previews/{item['id']}.png"
        data=preview(item)
        thumbnails[fname]=data
        item["preview"]=fname
        item["preview_sha256"]=hashlib.sha256(data).hexdigest()
    catalog={"version":9, "name":"Vellora Online | Jewelry & Eyewear",
             "format":"vellora-head-jewelry-v1","presets":presets}
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        archive.writestr("catalog.json",json.dumps(catalog,ensure_ascii=False,separators=(",",":")).encode("utf-8"))
        for name, data in sorted(thumbnails.items()):
            archive.writestr(name,data)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist())==57
        parsed=json.loads(archive.read("catalog.json"))
        assert parsed["version"]==9 and len(parsed["presets"])==56
        for item in parsed["presets"]:
            assert hashlib.sha256(archive.read(item["preview"])).hexdigest()==item["preview_sha256"]
    print("VELLORA_V9_PACK_OK",str(output),output.stat().st_size, "bytes, 56 3D accessory presets + 56 PNG previews")

if __name__=="__main__":
    main()
