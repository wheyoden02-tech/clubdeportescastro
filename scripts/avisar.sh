#!/usr/bin/env bash
# Deja un comentario en el issue "Bitácora del robot de datos" del repositorio y menciona al dueño,
# así GitHub le envía el aviso por correo. Lo usa .github/workflows/datos-liga.yml.
#
# Uso: bash scripts/avisar.sh archivo_con_el_mensaje.md [--una-vez]
#   --una-vez: no repite el aviso si el último comentario del issue ya empieza igual
#              (evita recibir el mismo correo de error dos veces al día).
set -euo pipefail

mensaje="$1"
titulo="Bitácora del robot de datos"

num=$(gh issue list --state all --limit 200 --json number,title \
  --jq "map(select(.title == \"$titulo\")) | .[0].number // empty")
if [ -z "$num" ]; then
  url=$(gh issue create --title "$titulo" --body "Aquí el robot deja un comentario cuando actualiza la página (partidos, balance, plantilla), cuando empieza una temporada, en su revisión periódica y si algo falla. GitHub envía cada comentario por correo al dueño del repositorio.")
  num="${url##*/}"
fi

if [ "${2:-}" = "--una-vez" ]; then
  ultimo=$(gh issue view "$num" --json comments --jq '.comments[-1].body // ""' | head -n 1)
  if [ "$ultimo" = "$(head -n 1 "$mensaje")" ]; then
    echo "Este aviso ya se envió; no se repite."
    exit 0
  fi
fi

{ cat "$mensaje"; echo; echo "@${GITHUB_REPOSITORY_OWNER}"; } > "${RUNNER_TEMP:-/tmp}/aviso.md"
gh issue comment "$num" --body-file "${RUNNER_TEMP:-/tmp}/aviso.md"
