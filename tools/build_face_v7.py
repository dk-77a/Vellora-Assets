#!/usr/bin/env python3
"""Vellora v7: actual skinned Ara nose/mouth morphs plus illustrated previews.

The PNGs are UI illustrations, not separate GLBs. All shape values are
applied to the original animated 3D head by creator_face_geometry.gd.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from appearance_previews import preview

NOSES = [
 ("fino","Nariz fino",dict(width=-.75,projection=.04,lift=0,bridge=-.15)),
 ("largo","Nariz largo",dict(width=.70,projection=.05,lift=0,bridge=.10)),
 ("arrebitado","Nariz arrebitado",dict(width=-.10,projection=.08,lift=.82,bridge=-.10)),
 ("longo","Nariz alongado",dict(width=-.15,projection=.80,lift=-.55,bridge=.44)),
 ("pequeno","Nariz pequeno",dict(width=-.54,projection=-.56,lift=.25,bridge=-.30)),
 ("reto","Nariz reto",dict(width=-.12,projection=.25,lift=0,bridge=.65)),
 ("aquilino","Nariz aquilino",dict(width=.12,projection=.88,lift=-.35,bridge=.95)),
 ("arredondado","Nariz arredondado",dict(width=.42,projection=.42,lift=.28,bridge=-.25)),
 ("romano","Nariz romano",dict(width=.12,projection=.70,lift=-.25,bridge=.80)),
 ("delicado","Nariz delicado",dict(width=-.62,projection=-.12,lift=.16,bridge=-.30)),
 ("alto","Ponte nasal alta",dict(width=-.18,projection=.35,lift=.10,bridge=.90)),
 ("baixo","Ponte nasal baixa",dict(width=.16,projection=-.26,lift=.12,bridge=-.85)),
 ("curto","Nariz curto",dict(width=.05,projection=-.52,lift=.56,bridge=-.20)),
 ("marcado","Nariz marcado",dict(width=.25,projection=.62,lift=-.10,bridge=.52)),
 ("narinas_finas","Narinas finas",dict(width=-.83,projection=.15,lift=.08,bridge=.05)),
 ("suave","Nariz suave",dict(width=-.30,projection=-.06,lift=.20,bridge=.22)),
]
MOUTHS = [
 ("delicada","Boca delicada",dict(width=-.38,fullness=-.18,upper=-.12,lower=-.15)),
 ("volumosa","Lábios volumosos",dict(width=.15,fullness=.90,upper=.65,lower=.70)),
 ("fina","Lábios finos",dict(width=-.04,fullness=-.76,upper=-.65,lower=-.62)),
 ("larga","Boca larga",dict(width=.90,fullness=.12,upper=0,lower=0)),
 ("pequena","Boca pequena",dict(width=-.80,fullness=-.25,upper=-.15,lower=-.10)),
 ("coracao","Lábios coração",dict(width=-.25,fullness=.32,upper=.80,lower=.05,curl=.20)),
 ("superior","Lábio superior marcado",dict(width=.05,fullness=.16,upper=.95,lower=-.14)),
 ("inferior","Lábio inferior cheio",dict(width=.05,fullness=.20,upper=-.10,lower=.98)),
 ("sorriso","Lábios com sorriso",dict(width=.28,fullness=.18,upper=.12,lower=.20,curl=.62)),
 ("natural","Boca natural",dict(width=0,fullness=.04,upper=.02,lower=.05)),
 ("arco","Arco do cupido",dict(width=-.18,fullness=.40,upper=.96,lower=.25,curl=.08)),
 ("cheia","Boca preenchida",dict(width=.10,fullness=.72,upper=.42,lower=.90)),
 ("discreta","Boca discreta",dict(width=-.45,fullness=-.43,upper=-.38,lower=-.36)),
 ("marcada","Contorno marcado",dict(width=.14,fullness=.32,upper=.62,lower=.47)),
 ("suave","Contorno suave",dict(width=-.12,fullness=-.08,upper=.14,lower=.10)),
 ("larga_cheia","Lábios largos",dict(width=.72,fullness=.46,upper=.28,lower=.55)),
]

def make_catalog():
    entries=[]
    for category,options in (("nose",NOSES),("mouth",MOUTHS)):
        for slug,label,shape in options:
            assert all(-1.0 <= float(v) <= 1.0 for v in shape.values())
            entries.append(dict(id=f"v7_{category}_{slug}",category=category,label=label,shape=shape))
    assert len(entries)==32 and len({p["id"] for p in entries})==32
    return dict(version=7,product="Vellora Online",format="makehuman-procedural-face-geometry-v2",presets=entries)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="Vellora-Ara-Face-Details-v7.zip")
    args=parser.parse_args()
    path=Path(args.out)
    path.parent.mkdir(parents=True,exist_ok=True)
    catalog=make_catalog()
    images={}
    for p in catalog["presets"]:
        filename=f"previews/{p['id']}.png"
        data=preview(p)
        images[filename]=data
        p["preview"]=filename
        p["preview_sha256"]=hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as dest:
        dest.writestr("catalog.json",json.dumps(catalog,ensure_ascii=False,separators=(",",":")).encode())
        for filename,data in sorted(images.items()):
            dest.writestr(filename,data)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None and len(z.namelist())==33
        d=json.loads(z.read("catalog.json"))
        assert len(d["presets"])==32
        for p in d["presets"]:
            assert hashlib.sha256(z.read(p["preview"])).hexdigest()==p["preview_sha256"]
    print("VELLORA_V7_PACK_OK",path,path.stat().st_size,"bytes: 32 skinned morphs + 32 preview PNG")

if __name__=="__main__":
    main()
