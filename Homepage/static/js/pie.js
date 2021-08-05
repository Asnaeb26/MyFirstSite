$(document).ready(function(){
    $.post(
       window.graphic_url, {},
        function (response) {
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
);
});

