const video = document.querySelector("#giro");
const button = document.querySelector(".playback");
const motion = matchMedia("(prefers-reduced-motion: reduce)");
let wantsPlayback = !motion.matches;
let visible = false;

function updatePlayback() {
  if (wantsPlayback && visible && !document.hidden) {
    video.play().catch(() => {});
  } else {
    video.pause();
  }
}

button.hidden = false;
video.controls = false;
button.addEventListener("click", () => {
  wantsPlayback = video.paused;
  updatePlayback();
});
video.addEventListener("play", () => button.textContent = "Pausar giro");
video.addEventListener("pause", () => button.textContent = "Reproducir giro");
motion.addEventListener("change", () => {
  wantsPlayback = !motion.matches;
  updatePlayback();
});
document.addEventListener("visibilitychange", updatePlayback);
new IntersectionObserver(([entry]) => {
  visible = entry.isIntersecting;
  updatePlayback();
}, { threshold: 0.15 }).observe(video);
