// ===================================================
// 1. 시계 기능
// ===================================================
(function setupClock() {
    const clockElement = document.getElementById('clock');
    if (!clockElement) return;

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

    updateClock(); // 즉시 실행
    setInterval(updateClock, 1000); // 1초마다 업데이트
})();


// ===================================================
// 2. 이미지 캐러셀(슬라이드) 기능
// ===================================================
(function setupCarousel() {
    const track = document.querySelector('.track');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    if (!track || !prevButton || !nextButton) return;
    
    const slides = Array.from(track.children);
    let currentIndex = 0;

    function updateSlidePosition() {
        if (slides.length === 0) return; // 슬라이드가 없을 경우 오류 방지
        const slideWidth = slides[0].getBoundingClientRect().width;
        const offset = -currentIndex * slideWidth;
        track.style.transform = `translateX(${offset}px)`;
        
        // 버튼 활성화/비활성화
        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex === slides.length - 1;
    }

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateSlidePosition();
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
            updateSlidePosition();
        }
    });

    // 창 크기 변경 시 슬라이드 위치 재조정
    window.addEventListener('resize', updateSlidePosition);
    
    // 초기화
    updateSlidePosition();
})();


// ===================================================
// 3. 실시간 그래프 업데이트 기능 (5초 주기)
// ===================================================
(function setupRealtimeGraph() {
    const graphImage = document.getElementById('graph-image');
    if (!graphImage) return;

    function updateGraph() {
        // 이미지 URL에 현재 시간을 쿼리 파라미터로 추가하여 캐시 방지
        const baseURL = graphImage.dataset.src;
        graphImage.src = `${baseURL}?t=${new Date().getTime()}`;
    }

    updateGraph(); // 즉시 실행
    setInterval(updateGraph, 5000); // 5초마다 업데이트
})();


// ===================================================
// 4. 실시간 혼잡도 정보 업데이트 기능 (5초 주기)
// ===================================================
(function setupCongestionStatus() {
    const populationDiv = document.querySelector('.population-details');
    if (!populationDiv) return;

    const countElement = document.getElementById('population-count');
    const congestionElement = document.getElementById('congestion-steps'); // 변수 이름 수정 (CongestionElement -> congestionElement)
    const iconElement = document.getElementById('density_Icon');
    const apiUrl = populationDiv.dataset.url;

    if (!countElement || !congestionElement || !iconElement || !apiUrl) return;

    // 혼잡도 상태에 따라 아이콘과 색상을 변경하는 함수
    function updateIcon(label) {
        let newIconClass = '';
        let newColor = '';

        switch (label) {
            case "원활":
                newIconClass = 'fa-solid fa-face-grin-beam fa-8x';
                newColor = '#5cb85c'; // 초록색
                break;
            case "보통":
                newIconClass = 'fa-solid fa-face-meh fa-8x';
                newColor = '#f0ad4e'; // 주황색
                break;
            case "혼잡":
                newIconClass = 'fa-solid fa-face-frown fa-8x';
                newColor = '#d9534f'; // 빨간색
                break;
            case "매우 혼잡":
                newIconClass = 'fa-solid fa-face-dizzy fa-8x';
                newColor = '#000000';
                break;

            default: // '오류' 또는 알 수 없는 값
                newIconClass = 'fa-solid fa-face-sad-tear fa-8x';
                newColor = '#f700ffff';
                break;
        }
        iconElement.className = newIconClass;
        iconElement.style.color = newColor;
    }

    // API를 호출하여 혼잡도 데이터를 가져오고 UI를 업데이트하는 함수
    function updateStatus() {
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                countElement.textContent = `${data.object_count}명`;
                congestionElement.textContent = data.label;
                updateIcon(data.label);
            })
            .catch(error => {
                console.error('혼잡도 데이터를 불러오는 데 실패했습니다:', error);
                countElement.textContent = '오류';
                congestionElement.textContent = '알 수 없음';
                updateIcon('오류');
            });
    }

    updateStatus(); // 즉시 실행
    setInterval(updateStatus, 5000); // 5초마다 업데이트
})();


// ===================================================
// 5. 실시간 영상 모달 팝업 기능
// ===================================================
(function setupVideoModal() {
    const openModalBtn = document.getElementById('open-video-modal');
    const closeModalBtn = document.getElementById('close-video-modal');
    const modalOverlay = document.getElementById('video-modal-overlay');

    if (!openModalBtn || !closeModalBtn || !modalOverlay) return;

    // 모달 열기
    function openModal() {
        modalOverlay.classList.remove('hidden');
    }

    // 모달 닫기
    function closeModal() {
        modalOverlay.classList.add('hidden');
    }

    // 이벤트 리스너 등록
    openModalBtn.addEventListener('click', openModal);
    closeModalBtn.addEventListener('click', closeModal);
    
    // 모달 바깥 영역 클릭 시 닫기
    modalOverlay.addEventListener('click', (event) => {
        if (event.target === modalOverlay) {
            closeModal();
        }
    });
})();