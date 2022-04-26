$(document).ready(function () {
    $('#Check').click(function (e) {
        let username = $('#username').val()
        if (username.length <= 3) {
            e.preventDefault()
            alert('Имя слишком короткое')
        }
    });
});


