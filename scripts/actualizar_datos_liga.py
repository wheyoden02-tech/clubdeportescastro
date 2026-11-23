"""Actualiza public/datos/liga.js con los últimos resultados y la plantilla de Deportes Castro.

Lee la ficha pública del equipo en lnbchile.com. No usa la API de la liga, que su
robots.txt reserva. Reglas:
- Si la ficha está pero viene sin partidos o sin jugadores (por ejemplo, al empezar
  una temporada), se conservan los datos anteriores y no hay error.
- Si la página ya no se reconoce (la liga la rediseñó), no se toca nada y el script
  termina con error para que GitHub avise por correo.

Uso: python scripts/actualizar_datos_liga.py [archivo_html_local]
"""
import json, os, re, sys, urllib.request
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
    datos["temporada"] = calcular_temporada(datos, anterior)
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
    resumen = resumir_cambios(anterior, datos)
    if resumen and os.environ.get("RESUMEN"):
        Path(os.environ["RESUMEN"]).write_text(resumen, encoding="utf-8")
    print(resumen or "Actualizado (sin cambios visibles en la página).")


def anio(partido):
    return int(partido["fecha"][:4])


def calcular_temporada(datos, anterior):
    """Año que se muestra sobre la plantilla. Normalmente es el del último partido, pero si la
    liga publica una plantilla nueva antes del primer partido del año, se usa el año actual."""
    temporada = max(anterior.get("temporada") or 0, anio(datos["partidos"][0]) if datos["partidos"] else 0)
    ids = lambda lista: {j["id"] for j in lista or []}
    if ids(datos["plantilla"]) - ids(anterior.get("plantilla")) and date.today().year > temporada:
        temporada = date.today().year
    return temporada or None


def legible(nombre):
    apellido, _, inicial = nombre.partition(",")
    return (inicial.strip() + " " + apellido.strip().title()).strip()


def resumir_cambios(anterior, datos):
    """Explica en palabras simples qué cambió, para avisar al dueño del sitio."""
    lineas = []
    viejos = {p["enlace"] for p in anterior.get("partidos", [])}
    nuevos = [p for p in reversed(datos["partidos"]) if p["enlace"] not in viejos]
    if anterior.get("temporada") and datos["temporada"] and datos["temporada"] > anterior["temporada"]:
        lineas.append(f"**Empezó la temporada {datos['temporada']}.** La página ya muestra el nuevo año.")
    formato = lambda f: f"{int(f[8:10])}/{int(f[5:7])}/{f[:4]}"
    for p in nuevos:
        resultado = "ganó" if p["gano"] else "perdió"
        lugar = "de local" if p["local"] else "de visita"
        lineas.append(f"Nuevo partido ({formato(p['fecha'])}, {lugar}): Castro {resultado} "
                      f"{p['castro']}-{p['rivalPuntos']} contra {p['rival']}.")
    if anterior.get("record") and datos["record"] != anterior.get("record"):
        lineas.append(f"Balance del torneo: {anterior['record']} → {datos['record']}.")
    antes = {j["id"]: j for j in anterior.get("plantilla", [])}
    ahora = {j["id"]: j for j in datos["plantilla"]}
    llegan = [ahora[i] for i in ahora if i not in antes]
    salen = [antes[i] for i in antes if i not in ahora]
    if llegan:
        lineas.append("Jugadores nuevos en la plantilla: " + ", ".join(f"#{j['numero']} {legible(j['nombre'])}" for j in llegan) + ".")
        complementos = SALIDA.parent / "plantilla.js"
        conocidos = set(re.findall(r'"(\d+)"\s*:', complementos.read_text(encoding="utf-8"))) if complementos.exists() else set()
        sin_nombre = [j for j in llegan if j["id"] not in conocidos]
        if sin_nombre:
            lineas.append("Se muestran con el nombre abreviado de la liga (" + ", ".join(legible(j["nombre"]) for j in sin_nombre)
                          + "). Es opcional: si quieres su nombre completo y posición, pídeselo a un agente.")
    if salen:
        lineas.append("Ya no aparecen en la ficha de la liga: " + ", ".join(legible(j["nombre"]) for j in salen) + ".")
    if not lineas:
        return ""
    return "\n".join(["**Se actualizaron los datos de deportescastro.cl**", ""] + [f"- {l}" for l in lineas]
                     + ["", "Revisa la página: https://deportescastro.cl"])


if __name__ == "__main__":
    main()
