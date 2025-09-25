const clockElement = document.getElementById('clock');

function updateClock() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const date = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    clockElement.textContent = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
}
setInterval(updateClock, 1000);
updateClock();

const track = document.querySelector('.track');
const slides = Array.from(track.children);
const prev = document.querySelector('.prev');
const next = document.querySelector('.next');
let index = 0;

function update() {
  const offset = -index * slides[0].getBoundingClientRect().width;
  track.style.transform = `translateX(${offset}px)`;
  prev.disabled = index === 0;
  next.disabled = index === slides.length - 1;
}

prev.addEventListener('click', () => { index = Math.max(0, index - 1); update(); });
next.addEventListener('click', () => { index = Math.min(slides.length - 1, index + 1); update(); });

window.addEventListener('resize', update);
update();
