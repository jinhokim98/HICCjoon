function valid_check(e) {
    const grading_file = document.getElementById('input_grading_file');
    const file_form = /(.*?)\.(py)$/;
    const file_path = grading_file.value;

    if (!file_form.exec(file_path)) {
        document.getElementById('file_uploaded').textContent = "please input .py file.";
        grading_file.value = '';
        return false;
    } else {
        document.getElementById('file_uploaded').textContent = "";
        return true;
    }

}
