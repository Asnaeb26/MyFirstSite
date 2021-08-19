$(document).ready(function(){
    $.post(
       window.graphic_url, {},
        function (response) {
        var options = {
            data: [{
                type: "doughnut",
                startAngle: 40,
                explodeOnClick: false,
                toolTipContent: "<b>{label}</b>: {per}%",
                showInLegend: "true",
                legendText: "{label}",
                indexLabelFontSize: 16,
                indexLabel: "{label} - {per}% ({y} BYN)",
                dataPoints: response
            }]
        };
        console.log(response)
        $("#chartContainer").CanvasJSChart(options);
        }
);
});

