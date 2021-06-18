$( document ).ready(function () {
    $('#Enter1').click(function (e) {
        x = $('#username').val()
        if (x.length <= 3) {
            e.preventDefault()
            alert('Имя слишком короткое')
        }

    })

    $('#Enter1').click(function (e) {
        x = $('#password').val()
        if (x.length <= 4) {
            e.preventDefault()
            alert('Пароль слишком простой')
        }

    })

})

