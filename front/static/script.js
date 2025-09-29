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

// 그래프를 업데이트하는 함수를 따로 만듭니다.
function updateGraph() {
    const graphImage = document.getElementById('graph-image');
    if (graphImage) {
        // ✨ 핵심: 캐시(Cache) 방지를 위해 URL 뒤에 현재 시간을 덧붙입니다.
        // 이렇게 하면 브라우저는 매번 새로운 이미지라고 인식하여 서버에 다시 요청합니다.
        const url = graphImage.dataset.src;
        graphImage.src = url + '?t=' + new Date().getTime();
    }
}

// 페이지가 처음 로드될 때 한 번 즉시 실행
updateGraph();

// 그 후 5초(5000밀리초)마다 updateGraph 함수를 계속해서 실행
setInterval(updateGraph, 5000);

const populationDiv = document.querySelector('.population-details');
const countElement = document.getElementById('population-count');
const CongestionElement = document.getElementById('congestion-steps');
//const value = 0;

// 2. HTML에 저장해둔 API URL을 가져옵니다.
const apiUrl = populationDiv.dataset.url;

// 3. 혼잡도 데이터를 요청하고 화면을 업데이트하는 함수를 만듭니다.
function updateCongestionStatus() {
    fetch(apiUrl) // API에 데이터 요청
        .then(response => response.json()) // 응답을 JSON 형태로 변환
        .then(data => {
            // JSON 데이터에서 object_count 값을 사용해 화면의 텍스트를 변경
            // 예: data = {"level": 3, "label": "혼잡", "object_count": 52}
            countElement.textContent = `${data.object_count}명`;
            //value = parseInt(data.object_count);
            CongestionElement.textContent = `${data.label}`;
        })
        .catch(error => {
            // 에러가 발생하면 콘솔에 출력
            console.error('데이터를 불러오는 데 실패했습니다:', error);
            countElement.textContent = '오류';
        });
}

// 4. 페이지가 처음 로드될 때 한번 실행하고,
updateCongestionStatus();

// 5. 그 후 5초(5000ms)마다 주기적으로 함수를 반복 실행합니다. (시간은 조절 가능)
setInterval(updateCongestionStatus, 5000);

// 혼잡도 수치에 따라 아이콘과 색상을 업데이트하는 함수
function density_Icon(value) {
    const iconElement = document.getElementById('density_Icon');
    const valueElement = document.getElementById('population-count');
    let newIconClass = '';
    let newColor = '';

    // 1. 값에 따라 아이콘 클래스와 색상을 결정합니다.
    if (value <= 30) { // 0~30: 원활
        newIconClass = 'fa-solid fa-face-grin-beam fa-8x';
        newColor = '#5cb85c'; // 초록색
    } else if (value <= 50 && value > 30) { // 31~70: 보통
        newIconClass = 'fa-solid fa-face-meh fa-8x';
        newColor = '#f0ad4e'; // 주황색
    } else if (value > 50 && value <= 71) { // 71 이상: 혼잡
        newIconClass = 'fa-solid fa-face-frown fa-8x';
        newColor = '#d9534f'; // 빨간색
    }
    else {
        newIconClass = 'fa-solid fa-face-dizzy fa-8x';
        newColor = '#000000ff';
    }

    // 2. 아이콘 요소의 클래스와 스타일을 변경합니다.
    // className을 통째로 바꿔서 'fa-solid fa-2x'는 유지하고 아이콘 이름만 교체합니다.
    iconElement.className = newIconClass; 
    iconElement.style.color = newColor;

    // 3. 화면에 현재 값도 표시해 줍니다.
    valueElement.textContent = value;
}

// === 함수 테스트 ===
// updateCongestionIcon(25);  // 원활 아이콘 표시
// updateCongestionIcon(65);  // 보통 아이콘 표시
density_Icon(72);  // 혼잡 아이콘 표시


// ===================================================
// 실시간 영상 모달 기능
// ===================================================

// 1. 필요한 HTML 요소들을 선택합니다.
const openModalBtn = document.getElementById('open-video-modal');
const closeModalBtn = document.getElementById('close-video-modal');
const modalOverlay = document.getElementById('video-modal-overlay');

// 2. 모달을 여는 함수
function openModal() {
    modalOverlay.classList.remove('hidden');
}

// 3. 모달을 닫는 함수
function closeModal() {
    modalOverlay.classList.add('hidden');
}

// 4. '실시간 영상' 버튼 클릭 시 모달 열기
openModalBtn.addEventListener('click', openModal);

// 5. 'X' 버튼 클릭 시 모달 닫기
closeModalBtn.addEventListener('click', closeModal);

// 6. 팝업 바깥의 어두운 영역 클릭 시 모달 닫기
modalOverlay.addEventListener('click', function(event) {
    // 만약 클릭된 곳이 어두운 배경(overlay) 자신이라면
    if (event.target === modalOverlay) {
        closeModal();
    }
});