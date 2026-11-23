(() => {
  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };

  const resultados = window.LIGA;
  const dia = (f) => new Date(f + "T12:00:00");
  const ultimo = resultados && resultados.partidos && resultados.partidos.length ? dia(resultados.partidos[0].fecha) : null;
  const terminada = ultimo && Date.now() - ultimo > 30 * 864e5;
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
        (p.local ? "Local" : "Visita") + " · " + formato.format(dia(p.fecha))));
      const score = el("span", "game-score", p.castro + " – " + p.rivalPuntos);
      a.append(badge, info, score);
      li.append(a);
      lista.append(li);
    }
    const record = document.getElementById("record");
    if (record && resultados.record) {
      const [g, pe] = resultados.record.split("-");
      record.textContent = "Balance del torneo: " + g + " ganados · " + pe + " perdidos";
    }
    const aviso = document.getElementById("aviso-temporada");
    if (aviso && terminada) {
      aviso.textContent = "Sin partidos en las últimas semanas. Las próximas fechas se publican en el calendario oficial de la liga.";
      aviso.hidden = false;
    }
  } else {
    const s = document.getElementById("partidos");
    if (s) s.hidden = true;
  }

  // La lista sale de la LNB (liga.js); plantilla.js aporta nombres completos, posiciones y entrenador.
  const extra = window.PLANTILLA || {};
  const nombres = extra.nombres || {};
  const legible = (n) => {
    const [apellido, inicial] = n.split(",").map((x) => x.trim());
    const bonito = apellido.toLowerCase().replace(/(^|[\s-])\p{L}/gu, (c) => c.toUpperCase());
    return inicial ? inicial + " " + bonito : bonito;
  };
  const grilla = document.getElementById("lista-plantilla");
  const lista2 = resultados && resultados.plantilla;
  if (grilla && lista2 && lista2.length) {
    const jugadores = [...lista2].sort((a, b) => a.numero - b.numero);
    for (const j of jugadores) {
      const info = nombres[j.id] || {};
      const li = el("li", "player");
      li.append(el("span", "player-num", String(j.numero)), el("b", null, info.nombre || legible(j.nombre)));
      if (info.posicion) li.append(el("small", null, info.posicion));
      grilla.append(li);
    }
    const t = document.getElementById("titulo-plantilla-sub");
    const anio = resultados.temporada || (ultimo && ultimo.getFullYear());
    if (t && anio) t.textContent = "Temporada " + anio;
    const dt = document.getElementById("entrenador");
    if (dt && extra.entrenador) dt.textContent = extra.entrenador;
    else if (dt) dt.parentElement.hidden = true;
  } else {
    const s = document.getElementById("plantilla");
    if (s) s.hidden = true;
  }

  // La camiseta (video) y su imagen fija se descargan recién cuando el visitante se acerca a esa
  // sección, para no competir con la carga inicial. Con "reducir movimiento" se queda en la imagen fija.
  const giro = document.querySelector("video.giro");
  if (giro) {
    const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const activar = () => {
      if (!giro.poster) giro.poster = giro.dataset.poster;
      if (quieto) return;
      if (!giro.getAttribute("src")) giro.src = giro.dataset.src;
      giro.play().catch(() => {});
    };
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(([e]) => {
        if (e.isIntersecting) activar();
        else if (giro.getAttribute("src")) giro.pause();
      }, { rootMargin: "300px 0px" }).observe(giro);
    } else {
      activar();
    }
  }
})();
