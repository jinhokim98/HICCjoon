const join_name = document.querySelector('#join_name');
const join_id = document.querySelector('#join_id');
const join_pw = document.querySelector('#join_pw');
const join_check_pw = document.querySelector('#join_confirm_pw');

const join_row = {
    name: {
        'tag' : join_name,
        'invalid': false,
    },
    id_: {
        'tag': join_id,
        'invalid': false,
    },
    pw: {
        'tag': join_pw,
        'invalid': false,
    },
}


function valid_check() {
    for (const key in join_row) {
        join_row[key]['invalid'] = false;

        join_row[key]['tag'].addEventListener("invalid", function(e) {
            show_error(join_row[key]['tag']);
            join_row[key]['invalid'] = true;
            e.preventDefault();
        });

        if (join_row[key]['invalid'] === false) {
            show_nothing(join_row[key]['tag']);
        }
    }

    is_difference_password();
}

function show_error(invalid) {
    if (invalid === join_name) {
        document.querySelector('#name_err_message').innerHTML = "2~5자의 한글을 사용하세요.";
    } else if (invalid === join_id) {
        document.querySelector('#id_err_message').innerHTML = "4~16자의 영문, 숫자를 사용하세요.";
    } else if (invalid === join_pw) {
        document.querySelector('#pw_err_message').innerHTML = "8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.";
    }
}

function show_nothing(valid) {
    if (valid === join_name) {
        document.querySelector('#name_err_message').innerHTML = '';
    } else if (valid === join_id) {
        document.querySelector('#id_err_message').innerHTML = '';
    } else if (valid === join_pw) {
        document.querySelector('#pw_err_message').innerHTML = '';
    }
}

function is_difference_password() {
    if (join_pw.value !== join_check_pw.value) {
        document.querySelector('#pw_confirm_err_message').innerHTML = "비밀번호가 같지 않습니다.";
        return false;

    } else {
        document.querySelector('#pw_confirm_err_message').innerHTML = "";
        return true;
    }
}

document.querySelector('#signup_btn').addEventListener('click', valid_check);

if (id_duplicate === "True") {
    alert("아이디 중복입니다.")
}