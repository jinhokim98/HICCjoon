const submit_button = document.getElementById("submit");
const code_editor = document.getElementById("code");
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
    var http = new XMLHttpRequest();
    var number = "{% task_index %}" // 이거 가져오기만 하면 되는데 여기가 안되네
    http.open("POST", "task/" + number, true);
    
    var language = document.getElementById("language").selectedOptions[0].value;
    var source_code = document.getElementById("code").innerText
    var jsonData = {"language" : language , "code" : source_code};

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
        document.getElementById("code").innerText = "";
    }
}



submit_button.addEventListener("click", submit_code);
language_selector.addEventListener("change", confirm_language);
// codeEditor.addEventListener("input", refresh_highlight);