#!/usr/bin/env python3
"""Vellora v8 - reproducible, original makeup and facial-tattoo pack."""
import argparse, hashlib, io, json, zipfile, math
from pathlib import Path
from PIL import Image, ImageDraw
from appearance_previews import preview

PAL = {
    "eyeshadow": [
        ("natural", "Olhar natural", "#916758", .28),
        ("chocolate", "Marrom esfumado", "#4a2b25", .53),
        ("preto", "Preto noturno", "#17151d", .77),
        ("violeta", "Violeta urbano", "#67409d", .68),
        ("azul", "Azul profundo", "#205b9c", .68),
        ("rose", "Rosé elegante", "#ba6384", .52),
        ("cobre", "Cobre metalizado", "#b46f45", .68),
        ("esmeralda", "Esmeralda", "#277668", .64),
    ],
    "lipstick": [
        ("nude","Nude suave","#b67e6f",.38),("rosa","Rosa claro","#dd7693",.66),
        ("vinho","Vinho intenso","#7e2445",.82),("vermelho","Vermelho clássico","#c73646",.85),
        ("cereja","Cereja escuro","#a4274a",.82),("marrom","Marrom café","#704238",.74),
        ("coral","Coral vivo","#d75b53",.73),("gloss","Gloss rosado","#ee9aa8",.43),
    ],
    "blush": [
        ("rose","Rosado natural","#c7657d",.40),("pessego","Pêssego","#dc8d64",.40),
        ("bronze","Bronzeado","#98633b",.45),("framboesa","Framboesa","#a8486d",.38),
        ("lavanda","Lavanda","#b17aa8",.33),("coral","Coral","#d96960",.40),
    ],
    "lashes": [
        ("natural","Naturais","#191923",.10),("delicado","Delicados","#302028",.20),
        ("castanho","Castanho suave","#453027",.28),("definido","Definidos","#111119",.45),
        ("volume","Volume intenso","#12121a",.70),("alongado","Alongados","#191821",.78),
        ("gatinho","Olhar gatinho","#15151f",.85),("dramatico","Dramáticos","#09090f",.95),
    ],
}
TATTOOS = [
    ("estrela","Estrela no rosto"),("lua","Lua crescente"),("raio","Raio urbano"),
    ("coracao","Coração delicado"),("lagrima","Lágrima"),("flor","Flor minimalista"),
    ("tribal","Traços tribais"),("coroa","Coroa pequena"),
    ("espiral","Espiral delicada"),("asa","Asa pequena"),
    ("folha","Folha minimalista"),("constelacao","Constelação"),
    ("geometrico","Triângulos"),("borboleta","Borboleta"),
    ("estrela_dupla","Estrelas duplas"),("onda","Onda urbana"),
]

def create_tattoo(kind):
    size=512
    image=Image.new("RGBA",(size,size),(0,0,0,0))
    draw=ImageDraw.Draw(image)
    ink=(23,20,31,240)
    def pt(x,y):return (int(x*size),int(y*size))
    def poly(points):draw.polygon([pt(*p) for p in points],fill=ink)
    def line(points,width=12):draw.line([pt(*p) for p in points],fill=ink,width=width,joint="curve")
    if kind=="estrela":
        poly([(.5+(.35 if i%2==0 else .15)*math.cos(i*math.pi/5-math.pi/2),
               .5+(.35 if i%2==0 else .15)*math.sin(i*math.pi/5-math.pi/2)) for i in range(10)])
    elif kind=="lua":
        draw.ellipse((pt(.12,.12),pt(.88,.88)),fill=ink)
        draw.ellipse((pt(.38,.04),pt(.97,.75)),fill=(0,0,0,0))
    elif kind=="raio":
        poly([(.56,.09),(.21,.53),(.50,.53),(.34,.93),(.84,.35),(.55,.35)])
    elif kind=="coracao":
        draw.ellipse((pt(.15,.17),pt(.55,.59)),fill=ink)
        draw.ellipse((pt(.45,.17),pt(.85,.59)),fill=ink)
        poly([(.15,.44),(.85,.44),(.5,.93)])
    elif kind=="lagrima":
        poly([(.5,.07),(.20,.62),(.28,.83),(.50,.94),(.72,.83),(.80,.62)])
    elif kind=="flor":
        for i in range(5):
            a=i*2*math.pi/5
            x=.50+.19*math.cos(a);y=.45+.19*math.sin(a)
            draw.ellipse((pt(x-.12,y-.12),pt(x+.12,y+.12)),fill=ink)
        draw.ellipse((pt(.45,.40),pt(.55,.50)),fill=(235,232,230,220))
        line([(.50,.67),(.50,.94)],9)
    elif kind=="tribal":
        line([(.14,.72),(.33,.50),(.53,.37),(.87,.13)],24)
        line([(.11,.77),(.42,.77),(.76,.52)],18)
        poly([(.43,.39),(.52,.16),(.62,.41)])
    elif kind=="coroa":
        poly([(.10,.30),(.32,.52),(.5,.13),(.68,.52),(.90,.30),(.79,.82),(.19,.82)])
    elif kind=="espiral":
        line([(.50+.39*(1-t/90)*math.cos(t*.14),.50+.39*(1-t/90)*math.sin(t*.14)) for t in range(91)],13)
    elif kind=="asa":
        poly([(.12,.55),(.38,.20),(.90,.14),(.73,.47),(.45,.78),(.21,.83)])
        line([(.25,.66),(.69,.36),(.87,.20)],7)
    elif kind=="folha":
        poly([(.21,.80),(.25,.37),(.59,.13),(.79,.19),(.86,.52),(.62,.79)])
        line([(.30,.75),(.72,.26)],9)
    elif kind=="constelacao":
        dots=[(.18,.29),(.36,.18),(.66,.29),(.79,.55),(.53,.82),(.22,.72)]
        line(dots,6)
        for x,y in dots: draw.ellipse((pt(x-.047,y-.047),pt(x+.047,y+.047)),fill=ink)
    elif kind=="geometrico":
        poly([(.5,.09),(.91,.83),(.09,.83)])
        draw.polygon([pt(*v) for v in [(.5,.38),(.67,.72),(.33,.72)]],fill=(0,0,0,0))
    elif kind=="borboleta":
        for cx in (.30,.70):
            draw.ellipse((pt(cx-.22,.17),pt(cx+.22,.56)),fill=ink)
            draw.ellipse((pt(cx-.17,.47),pt(cx+.17,.83)),fill=ink)
        line([(.5,.29),(.5,.81)],8)
    elif kind=="estrela_dupla":
        for cx,cy,sz in [(.30,.36,.24),(.69,.69,.18)]:
            poly([(cx+(sz if i%2==0 else sz*.42)*math.cos(i*math.pi/5-math.pi/2),
                   cy+(sz if i%2==0 else sz*.42)*math.sin(i*math.pi/5-math.pi/2)) for i in range(10)])
    elif kind=="onda":
        for y in (.36,.56,.76):
            line([(.09+i*.025,y+.065*math.sin(i*.28)) for i in range(33)],10)
    out=io.BytesIO()
    image.save(out,"PNG",optimize=True)
    return out.getvalue()

def build(dest):
    presets=[]
    for category, options in PAL.items():
        for slug,label,color,intensity in options:
            presets.append(dict(id=f"v8_{category}_{slug}", category=category,
                                label=label,color=color,intensity=intensity))
    images={}
    for slug,label in TATTOOS:
        file=f"tattoos/{slug}.png"
        binary=create_tattoo(slug)
        images[file]=binary
        presets.append(dict(id=f"v8_face_tattoo_{slug}",category="face_tattoo",
                            label=label,image=file,sha256=hashlib.sha256(binary).hexdigest(),
                            intensity=.85))
    assert len(presets)==46
    for spec in presets:
        file=f"previews/{spec['id']}.png"
        binary=preview(spec)
        images[file]=binary
        spec["preview"]=file
        spec["preview_sha256"]=hashlib.sha256(binary).hexdigest()
    catalog={"version":8,"name":"Vellora Online | Cosmetics & Face Art",
             "format":"vellora-cosmetics-v8","presets":presets}
    Path(dest).parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(dest,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as zipped:
        zipped.writestr("catalog.json",json.dumps(catalog,ensure_ascii=False).encode())
        for filename,data in images.items():
            zipped.writestr(filename,data)
    with zipfile.ZipFile(dest) as zipped:
        assert zipped.testzip() is None
        assert len(zipped.namelist()) == 1 + 16 + 46
        for spec in presets:
            if "image" in spec:
                assert hashlib.sha256(zipped.read(spec["image"])).hexdigest()==spec["sha256"]
            assert hashlib.sha256(zipped.read(spec["preview"])).hexdigest()==spec["preview_sha256"]
    print("VELLORA_V8_ZIP_OK",dest,Path(dest).stat().st_size,"bytes, 46 cosmetics and 46 preview PNG")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="Vellora-Ara-Cosmetics-v8.zip")
    args=p.parse_args()
    build(args.out)
