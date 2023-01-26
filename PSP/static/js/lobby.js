const remaining_time = document.getElementById('remaining_time');

function remaining_timer() {
    const now = new Date();
    const diff = contest_day - now;

    const diff_day = String(Math.floor(diff / (1000*60*60*24)));
    const diff_hour =String(Math.floor((diff / (1000*60*60)) % 24)).padStart(2,"0");
    const diff_min = String(Math.floor((diff / (1000*60)) % 60)).padStart(2,"0");
    const diff_sec = String(Math.floor(diff / 1000 % 60)).padStart(2,"0");

    remaining_time.textContent = `${diff_day}일 ${diff_hour}시간 ${diff_min}분 ${diff_sec}초 남았습니다.`;
}

function start_timer() {
    remaining_timer();
    setInterval(remaining_timer, 1000);
}

document.addEventListener('DOMContentLoaded', start_timer);

// https://codong.tistory.com/28
// https://nachwon.github.io/how-to-send-csrf-token-ajax/
function get_cookie(name) {
    let cookie_value = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookie_value;
}

const csrf_token = get_cookie('csrftoken');


function page_move() {
    // URL, META
fetch('lobby/', {
    method: "POST", 	// GET도 넣을 수는 있지만 안넣어도 상관없다. default는 get
    headers: {
        "Content-Type": "application/json",	// json형식의 값을 넘겨줌을 header에 명시
        "X-CSRFToken": csrf_token,
    },
    body: JSON.stringify({	//javascript 객체를 json객체로 변환한다.
    title: "Current Time",
    }),
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.contest);
        if (data.contest === "in_process") {
            window.location.replace('task/');
        }
        else if (data.contest === "end") {
            window.location.replace('end/');
        }
        setTimeout(page_move, 1000);
    })
    .catch(err => {

    });
}

setTimeout(page_move, 1000);