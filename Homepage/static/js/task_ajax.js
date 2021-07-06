// Сделать кнопку по нажатию на которую происходит ajax запрос на django.
// Django в свою очередь возвращает любое число и js отображает его с помощью alert
$(document).ready(function () {
    $('#task_ajax').click(function (e) {
        $.post('ajax_path',
            function (response) {
                alert(response.message)
            }
        );
    })

// Сделать проверку на уникальность логина с помощью ajax.
// Если такой уже занят то отображать табличку (есть красивые в bootstrap) с сообщением “Логин уже занят”.
// Подсказка: Сейчас если пытаться зарегать юзера с логином который уже есть, возникнет исключение.
// Вспоминаем как реагировать на исключения в python.
//     $('#')
    $('#username').blur(function () {
        $.post('uniq_user',
            {'a' : $('#username').val()},
                function(response) {
                if (response.message == 'y') {
                    alert('Такой логин уже есть')
                }
        })
    })
});