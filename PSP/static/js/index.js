const login_id = document.getElementById("id_");
const login_pw = document.getElementById("password");

const login_row = {
    id_: {
        'tag': login_id,
        'invalid': false,
    },
    pw: {
        'tag': login_pw,
        'invalid': false,
    },
}

function valid_check() {
    for (const key in login_row) {
        login_row[key]['invalid'] = false;

        login_row[key]['tag'].addEventListener("invalid", function(e) {
            show_error(login_row[key]['tag']);
            login_row[key]['invalid'] = true;
            e.preventDefault();
        });

        if (login_row[key]['invalid'] === false) {
            show_nothing(login_row[key]['tag']);
        }
    }

}

function show_error(invalid) {
    if (invalid === login_id) {
        document.getElementById('error_message').textContent = "아이디 오류 : 4~16자의 영문, 숫자를 사용하세요.";
    } else if (invalid === login_pw) {
        document.getElementById('error_message').textContent = "비밀번호 오류 : 8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.";
    }
}

function show_nothing(valid) {
    if (valid === login_id) {
        document.getElementById('error_message').textContent = "";
    } else if (valid === login_pw) {
        document.getElementById('error_message').textContent = "";
    }
}

document.getElementById('login_btn').addEventListener('click', valid_check);

if (Authenticate_fail === "True") {
    alert("비밀번호가 다릅니다.");
}

if (DoesNotExist === "True") {
    alert("존재하지 않는 계정입니다.");
}