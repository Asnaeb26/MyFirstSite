$(document).ready(function() {
        $("#plus_button").click(function(){
        $("#category").slideToggle("fast");
        $(this).toggleClass("active");
    })

    $('#id45').click(function (e){
        alert('Homepage tttttttttt')
    })

    $.post(
    "pie_fn", {}, [
        function fn1(response) {
        window.onload = function () {
        var options = {
            data: [{
                type: "pie",
                startAngle: 40,
                toolTipContent: "<b>{label}</b>: {y}%",
                showInLegend: "true",
                legendText: "{label}",
                indexLabelFontSize: 16,
                indexLabel: "{label} - {y}%",
                dataPoints: response
            }]
        };
        $("#chartContainer").CanvasJSChart(options);
}
            console.log(response)
        }
]);
});