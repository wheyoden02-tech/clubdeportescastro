(() => {
  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };

  const resultados = window.RESULTADOS;
  const lista = document.getElementById("lista-partidos");
  if (lista && resultados && resultados.partidos && resultados.partidos.length) {
    const formato = new Intl.DateTimeFormat("es-CL", { day: "numeric", month: "short" });
    for (const p of resultados.partidos) {
      const li = el("li", "game" + (p.gano ? " won" : " lost"));
      const a = el("a");
      a.href = p.enlace;
      a.rel = "noopener";
      const badge = el("span", "game-badge", p.gano ? "G" : "P");
      badge.title = p.gano ? "Ganado" : "Perdido";
      const info = el("span", "game-info");
      info.append(el("b", null, p.rival), el("small", null,
        (p.local ? "Local" : "Visita") + " · " + formato.format(new Date(p.fecha + "T12:00:00"))));
      const score = el("span", "game-score", p.castro + " – " + p.rivalPuntos);
      a.append(badge, info, score);
      li.append(a);
      lista.append(li);
    }
    const record = document.getElementById("record");
    if (record && resultados.record) {
      const [g, pe] = resultados.record.split("-");
      record.textContent = g + " ganados · " + pe + " perdidos";
    }
    const ultimo = new Date(resultados.partidos[0].fecha + "T12:00:00");
    const aviso = document.getElementById("aviso-temporada");
    if (aviso && Date.now() - ultimo > 30 * 864e5) {
      aviso.textContent = "La temporada " + ultimo.getFullYear() + " terminó. El calendario de la próxima se publica en la web de la liga.";
      aviso.hidden = false;
    }
  } else {
    const s = document.getElementById("partidos");
    if (s) s.hidden = true;
  }

  const plantilla = window.PLANTILLA;
  const grilla = document.getElementById("lista-plantilla");
  if (grilla && plantilla && plantilla.jugadores && plantilla.jugadores.length) {
    const jugadores = [...plantilla.jugadores].sort((a, b) => a.numero - b.numero);
    for (const j of jugadores) {
      const li = el("li", "player");
      li.append(el("span", "player-num", String(j.numero)), el("b", null, j.nombre));
      if (j.posicion) li.append(el("small", null, j.posicion));
      grilla.append(li);
    }
    const t = document.getElementById("titulo-plantilla-sub");
    if (t && plantilla.titulo) t.textContent = plantilla.titulo;
    const dt = document.getElementById("entrenador");
    if (dt && plantilla.entrenador) dt.textContent = plantilla.entrenador;
    else if (dt) dt.parentElement.hidden = true;
  } else {
    const s = document.getElementById("plantilla");
    if (s) s.hidden = true;
  }
})();
