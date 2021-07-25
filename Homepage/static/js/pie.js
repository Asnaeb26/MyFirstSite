$(document).ready(function(){
    const ARRAY =
        $.post(
        "pie_fn", {}, [
            function (response) {
                const array = [];
                for (let key in response) {
                    array.push([key, parseFloat(response[key])])
                }
                console.log(typeof array)
                console.log(array)
                return array
            }
       ]
    );
    // console.log(typeof ARRAY)
    // console.log(ARRAY)

  jQuery.jqplot.config.enablePlugins = true;

  const XX = [
    ['aaaa', 2323],
    ['Out of home', 623],
    ['Consument', 311],
    ['Bewerkende industrie', 590],
    ['Bewerkende industrie', 590],
    ['Bewerkende industrie', 590],
  ];


  plot7 = jQuery.jqplot('chart7',
    [
        [
            ['aaaa', 2323],
            ['Out of home', 623],
            ['Consument', 311],
            ['Bewerkende industrie', 590],
            ['Bewerkende industrie', 590],
            ['Bewerkende industrie', 590]
        ]
    ],
    {
      title: ' ',
      seriesDefaults: {shadow: true, renderer: jQuery.jqplot.PieRenderer, rendererOptions: { showDataLabels: true } },
      legend: { show:true }
    }
  );





});

window.onload = function () {

var options = {
	title: {
		text: "Desktop OS Market Share in 2017"
	},
	subtitles: [{
		text: "As of November, 2017"
	}],
	animationEnabled: false,
	data: [{
		type: "pie",
		startAngle: 40,
		toolTipContent: "<b>{label}</b>: {y}%",
		showInLegend: "true",
		legendText: "{label}",
		indexLabelFontSize: 16,
		indexLabel: "{label} - {y}%",
		dataPoints: [
			{ y: 48.36, label: "Windows 7" },
			{ y: 26.85, label: "Windows 10" },
			{ y: 1.49, label: "Windows 8" },
			{ y: 6.98, label: "Windows XP" },
			{ y: 6.53, label: "Windows 8.1" },
			{ y: 2.45, label: "Linux" },
			{ y: 3.32, label: "Mac OS X 10.12" },
			{ y: 4.03, label: "Others" }
		]
	}]
};
$("#chartContainer").CanvasJSChart(options);

}

