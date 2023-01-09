const submit_button = document.getElementById("submit");
const code_editor = document.getElementById("code");
const language_selector = document.getElementById("language");

// 마지막 코드 업데이트 후 스패밍 방지용 flag 하고 싶은데.. 일단은 보류
last_submit = 0;

// ajax code submittance
function submit_code(e){
    var http = new XMLHttpRequest();
    http.open("post", "task_details.html", true);

    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var params = "language=" + document.getElementById("language").selectedOptions[0].value
     + "&code=" + document.getElementById("code").innerText;
    http.send(params);

    http.onload = function(){
        alert(http.responseText);
    }
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