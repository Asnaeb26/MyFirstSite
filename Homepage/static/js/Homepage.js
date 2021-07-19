$(document).ready(function() {
    // $('#plus_button').click(function (e) {
    //     alert('Работает чтот-то')
    // })

    $("#plus_button").click(function(){
        $("#category").slideToggle("fast");
        $(this).toggleClass("active");
    });

});
