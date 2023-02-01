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


function get_statistics() {
    fetch('get_statistics/', {
    method: "POST", 	// GET도 넣을 수는 있지만 안넣어도 상관없다. default는 get
    headers: {
        "Content-Type": "application/json",	// json형식의 값을 넘겨줌을 header에 명시
        "X-CSRFToken": csrf_token,
    },
    body: JSON.stringify({	//javascript 객체를 json객체로 변환한다.
        title: "Request num of participants",
    }),
    })
    .then(res => res.json())
    .then(data => {
        document.querySelector('#participants').textContent = data.participants;
        document.querySelector('#submit_completed').textContent = data.submit_completed;

        let participants_info_inner = '';

        for (let idx = 0; idx < data.participants; idx++) {
            let sequence = idx + 1;
            participants_info_inner += '<tr>';
            participants_info_inner += '<th scope="row">' + sequence + '</th>';
            participants_info_inner += '<td>' + data.participants_detail[idx][0] + '</td>';
            participants_info_inner += '<td>' + data.participants_detail[idx][1] + '</td>';
            participants_info_inner += '</tr>';
        }

        let ranking_info_inner = '';

        for (let idx = 0; idx < data.participants; idx++) {
            let sequence = idx + 1;
            ranking_info_inner += '<tr>';
            ranking_info_inner += '<th scope="row">' + sequence + '</th>';
            ranking_info_inner += '<td>' + data.ranking_detail[idx][0] + '</td>';
            ranking_info_inner += '<td>' + data.ranking_detail[idx][1] + '</td>';
            ranking_info_inner += '</tr>';
        }

        document.querySelector('#participants_info').innerHTML = participants_info_inner;
        document.querySelector('#ranking_info').innerHTML = ranking_info_inner;

        setTimeout(get_statistics, 1000);
    })
}

setTimeout(get_statistics, 1000);
