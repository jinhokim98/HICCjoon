const submit_button = document.getElementById("submit");
const code_editor = document.getElementById("editor-code");
const language_selector = document.getElementById("language");

// 마지막 코드 업데이트 후 스패밍 방지용 flag 하고 싶은데.. 일단은 보류
last_submit = 0;

// https://codong.tistory.com/28
// https://nachwon.github.io/how-to-send-csrf-token-ajax/
function get_cookie(name) {
    var cookie_value = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookie_value;
}

var csrf_token = get_cookie('csrftoken');


// ajax code submittance
function submit_code(e){
    console.log("clicked submit");
    var http = new XMLHttpRequest();

    var url = window.location.href;
    http.open("POST", url, true);
    
    var language = document.getElementById("language").selectedOptions[0].value; 
    var source_code = document.getElementById("editor-code").innerText
    var jsonData = {"language" : language , "code" : source_code}; // 값 자체는 제대로 가져옴
    
    // http.onreadystatechange = function() {
    //     if (http.readyState == 4) {
    //         if (http.status == 200 || xhr.status == 201){
    //             console.log("[status] : " + xhr.status);
    //             console.log("[response] : " + "[success]");    				   				    				
    //             console.log("[response] : " + xhr.responseText);
    //             console.log("");        				
    //         }
    //         else {
    //             console.log("[status] : " + xhr.status);
    //             console.log("[response] : " + "[fail]");    				   				    				
    //             console.log("[response] : " + xhr.responseText);
    //             console.log("");        				 
    //         }						    				
    //     }    			
    // }

    http.setRequestHeader("Content-Type", "application/json");    		
    http.setRequestHeader("X-CSRFToken", csrf_token)
    http.send(JSON.stringify(jsonData));

    // http.onload = function(){
    //     alert(http.responseText);
    // }
}

function refresh_highlight(e){
    console.log(1);
    hljs.highlightElement(code_editor);
}

function confirm_language(e){
    if(confirm("언어를 변경할 경우 코드가 초기화됩니다.\n필요한 경우 백업해주세요.\n\n언어를 변경하시겠습니까?")){
        document.getElementById("editor-code").innerText = "";
    }
}

submit_button.addEventListener("click", submit_code);
language_selector.addEventListener("change", confirm_language);
// codeEditor.addEventListener("input", refresh_highlight);

const remaining_time = document.getElementById('remaining_time');

function remaining_timer() {
    const now = new Date();
    const diff = contest_end_time - now;

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

function page_move() {
    // URL, META
fetch('task_timecheck/', {
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
        if (data.contest === "end") {
            window.location.replace('end/');
        }
        setTimeout(page_move, 1000);
    })
    .catch(err => {

    });
}

setTimeout(page_move, 1000);