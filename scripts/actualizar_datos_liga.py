"""Actualiza public/datos/liga.js con los últimos resultados y la plantilla de Deportes Castro.

Lee la ficha pública del equipo en lnbchile.com. No usa la API de la liga, que su
robots.txt reserva. Reglas:
- Si la ficha está pero viene sin partidos o sin jugadores (por ejemplo, al empezar
  una temporada), se conservan los datos anteriores y no hay error.
- Si la página ya no se reconoce (la liga la rediseñó), no se toca nada y el script
  termina con error para que GitHub avise por correo.

Uso: python scripts/actualizar_datos_liga.py [archivo_html_local]
"""
import json, re, sys, urllib.request
from datetime import date
from pathlib import Path

FICHA = "https://lnbchile.com/liga/uno/equipos/17"
SALIDA = Path(__file__).resolve().parent.parent / "public" / "datos" / "liga.js"
SITEMAP = SALIDA.parent.parent / "sitemap.xml"
CABECERA = "// Archivo generado automáticamente por scripts/actualizar_datos_liga.py. No editar a mano.\n"
CODIGOS = {
    "UCA": "Universidad Católica", "COL": "Colo-Colo", "EST": "Español de Talca",
    "VAL": "CD Valdivia", "ANI": "Las Ánimas", "ANC": "ABA Ancud",
    "PVA": "Puerto Varas", "PMO": "Puerto Montt", "OSO": "Español de Osorno",
}


def leer_pagina():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
    req = urllib.request.Request(FICHA, headers={"User-Agent": "deportescastro.cl actualizador de datos"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def datos_de_pagina(html):
    trozos = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', html)
    return "".join(json.loads(t) for t in trozos)


def extraer_partidos(p):
    partidos = []
    patron = re.compile(
        r'"href":"/liga/uno/match/(?P<slug>[a-z0-9]+-vs-[a-z0-9]+-(?P<f>\d{4}-\d{2}-\d{2}))".*?'
        r'"children":"(?P<res>[GP])"\}.*?'
        r'"children":\["(?P<loc>@|vs)"," ","(?P<rival>[A-Z0-9]+)"\]\}.*?'
        r'"children":\[(?P<a>\d+),"-",(?P<b>\d+)\]'
    )
    for linea in p.split("\n"):
        m = patron.search(linea)
        if m:
            partidos.append({
                "fecha": m["f"],
                "local": m["loc"] == "vs",
                "rival": CODIGOS.get(m["rival"], m["rival"]),
                "castro": int(m["a"]),
                "rivalPuntos": int(m["b"]),
                "gano": m["res"] == "G",
                "enlace": "https://lnbchile.com/liga/uno/match/" + m["slug"],
            })
    partidos.sort(key=lambda x: x["fecha"], reverse=True)
    return partidos[:5]


def extraer_plantilla(p):
    jugadores, vistos = [], set()
    for fila in p.split('["$","tr","')[1:]:
        m = re.match(r'(?P<id>\d+)".*?"alt":"(?P<nombre>[^"]+)".*?"children":\["#","(?P<num>\d+)"\]', fila)
        if m and m["id"] not in vistos:
            vistos.add(m["id"])
            jugadores.append({"id": m["id"], "numero": int(m["num"]), "nombre": m["nombre"]})
    return jugadores


def extraer_record(p):
    m = re.search(r'"children":"Récord"\}\],\["\$","span",null,\{[^}]*"children":"(\d+-\d+)"', p)
    return m.group(1) if m else None


def leer_anterior():
    if not SALIDA.exists():
        return {}
    texto = SALIDA.read_text(encoding="utf-8")
    return json.loads(texto.split("=", 1)[1].strip().rstrip(";"))


def main():
    p = datos_de_pagina(leer_pagina())
    partidos, plantilla, record = extraer_partidos(p), extraer_plantilla(p), extraer_record(p)
    if record is None and not partidos and not plantilla:
        sys.exit("No reconozco la ficha del club: puede que la página de la liga haya cambiado.")

    anterior = leer_anterior()
    datos = {
        "fuente": FICHA,
        "record": record if partidos else anterior.get("record"),
        "partidos": partidos or anterior.get("partidos", []),
        "plantilla": plantilla or anterior.get("plantilla", []),
    }
    if datos == {k: anterior.get(k) for k in datos}:
        print("Sin cambios.")
        return
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(CABECERA + "window.LIGA = " + json.dumps(datos, ensure_ascii=False, indent=2) + ";\n",
                      encoding="utf-8")
    if SITEMAP.exists():  # avisa a Google que la portada cambió
        xml = SITEMAP.read_text(encoding="utf-8")
        SITEMAP.write_text(re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{date.today().isoformat()}</lastmod>", xml),
                           encoding="utf-8")
    print(f"Actualizado: {len(datos['partidos'])} partidos, {len(datos['plantilla'])} jugadores, récord {datos['record']}.")


if __name__ == "__main__":
    main()
