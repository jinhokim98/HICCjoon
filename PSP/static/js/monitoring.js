const remaining_time = document.getElementById('remaining_time');

function remaining_timer() {
    // views.py 에서 대회 종료 시간 받아 오면 new Date(contest_day)로 치환할 예정
    // contest_day 는 yyyy-mm-dd hh:mm:ss 로 formatting
    const now = new Date();

    const diff = contest_end_day - now;

    const diff_day = String(Math.floor(diff / (1000*60*60*24)));
    const diff_hour =String(Math.floor((diff / (1000*60*60)) % 24)).padStart(2,"0");
    const diff_min = String(Math.floor((diff / (1000*60)) % 60)).padStart(2,"0");
    const diff_sec = String(Math.floor(diff / 1000 % 60)).padStart(2,"0");

    remaining_time.textContent = `${diff_hour}시간 ${diff_min}분 ${diff_sec}초`;
}

function start_timer() {
    remaining_timer();
    setInterval(remaining_timer, 1000);
}

document.addEventListener('DOMContentLoaded', start_timer);