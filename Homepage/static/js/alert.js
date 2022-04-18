$(document).ready(function () {
    $('#Check').click(function (e) {
        let username = $('#username').val()
        let pass = $('#password').val()
        if (username.length <= 3) {
            e.preventDefault()
            alert('Имя слишком короткое')
        }
        if (pass.length <= 4) {
            e.preventDefault()
            alert('Пароль слишком простой')
        }
    });
});


