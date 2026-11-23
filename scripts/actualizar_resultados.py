"""Actualiza public/datos/resultados.js con los últimos resultados de Deportes Castro.

Lee la ficha pública del equipo en lnbchile.com (no usa la API de la liga, que su
robots.txt reserva). Si la página cambia de formato, no toca el archivo y termina con
error para que GitHub avise por correo.

Uso: python scripts/actualizar_resultados.py [archivo_html_local]
"""
import json, re, sys, urllib.request
from datetime import date
from pathlib import Path

FICHA = "https://lnbchile.com/liga/uno/equipos/17"
SALIDA = Path(__file__).resolve().parent.parent / "public" / "datos" / "resultados.js"
CODIGOS = {
    "UCA": "Universidad Católica", "COL": "Colo-Colo", "EST": "Español de Talca",
    "VAL": "CD Valdivia", "ANI": "Las Ánimas", "ANC": "ABA Ancud",
    "PVA": "Puerto Varas", "PMO": "Puerto Montt", "OSO": "Español de Osorno",
}


def leer_pagina():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
    req = urllib.request.Request(FICHA, headers={"User-Agent": "deportescastro.cl actualizador de resultados"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def datos_de_pagina(html):
    trozos = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', html)
    return "".join(json.loads(t) for t in trozos)


def extraer(p):
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
    rec = re.search(r'"children":"Récord"\}\],\["\$","span",null,\{[^}]*"children":"(\d+-\d+)"', p)
    return partidos, rec.group(1) if rec else None


def main():
    partidos, record = extraer(datos_de_pagina(leer_pagina()))
    if not partidos:
        sys.exit("No encontré resultados en la ficha: puede que la página de la liga haya cambiado.")
    partidos.sort(key=lambda x: x["fecha"], reverse=True)
    datos = {"fuente": FICHA, "record": record, "partidos": partidos[:5]}
    nuevo = "// Archivo generado automáticamente por scripts/actualizar_resultados.py. No editar a mano.\n" \
            "window.RESULTADOS = " + json.dumps(datos, ensure_ascii=False, indent=2) + ";\n"
    viejo = SALIDA.read_text(encoding="utf-8") if SALIDA.exists() else ""
    cuerpo = lambda s: s.split("window.RESULTADOS", 1)[-1]
    if cuerpo(viejo) != cuerpo(nuevo):
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(nuevo, encoding="utf-8")
        print(f"Actualizado: {len(datos['partidos'])} partidos, récord {record}.")
    else:
        print("Sin cambios.")


if __name__ == "__main__":
    main()
