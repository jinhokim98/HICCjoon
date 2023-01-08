const join_name = document.getElementById("join_name");
const join_id = document.getElementById("join_id");
const join_pw = document.getElementById("join_pw");
const join_check_pw = document.getElementById("join_check_pw");

const join_row = {
    name: join_name,
    id_ : join_id,
    pw: join_pw,
}

function valid_check() {
    for (const key in join_row) {
        join_row[key].addEventListener("invalid", function (e) {
            document.forms[0].classList.add("was-validated");
            show_error(join_row[key]);
            e.preventDefault();
        })

        join_row[key].addEventListener('input', function () {
            if (document.forms[0].classList.contains('was-validated')) {
                join_row[key].reportValidity();
            }
        })
    }
    is_difference_password();
}

function show_error(invalid) {
    if (invalid === join_name) {
        document.getElementById('name_err_message').textContent = "2~5자의 한글을 사용하세요.";
    } else if (invalid === join_id) {
        document.getElementById('id_err_message').textContent = "4~16자의 영문, 숫자를 사용하세요.";
    } else if (invalid === join_pw) {
        document.getElementById('pw_err_message').textContent = "8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.";
    }
}

function show_nothing(valid) {
    if (valid === join_name) {
        document.getElementById('name_err_message').textContent = "";
    } else if (valid === join_id) {
        document.getElementById('id_err_message').textContent = "";
    } else if (valid === join_pw) {
        document.getElementById('pw_err_message').textContent = "";
    }
}

function is_difference_password() {
    if (join_pw.value !== join_check_pw.value) {
        document.getElementById('pw_check_err_message').textContent = "비밀번호가 같지 않습니다.";
        return false;

    } else {
        document.getElementById('pw_check_err_message').textContent = "";
        return true;
    }
}

document.getElementById("signup_btn").addEventListener('click', valid_check);
