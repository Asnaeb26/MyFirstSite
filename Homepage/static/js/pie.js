$(document).ready(function(){
    $.post(
       window.graphic_url, {start: window.start, finish: window.finish},
        function (response) {
        var options = {
            data: [{
                type: "doughnut",
                startAngle: 40,
                explodeOnClick: false,
                // toolTipContent: "<b>{label}</b>: {per}%",
                toolTipContent: null,
                showInLegend: "true",
                legendText: "{label}",
                indexLabelFontSize: 16,
                indexLabel: "{label}: {per}% ({y} BYN)",
                dataPoints: response
            }]
        };
        console.log(response)
        $("#chartContainer").CanvasJSChart(options);
        }
);
});

