var pieChart = new Chart("pieChart", {
    type: "pie",
    data: {
        labels: ["Zaliczony", "Niezaliczony"],
        datasets: [{
            backgroundColor: ["green", "red"],
            data: [importPassed, importFailed],
            borderWidth: 0,
            
        }]
        },
        options: {
            responsive: true,
            plugins: {
                datalabels: {
                    formatter: function(value, context) {
                        return context.chart.data.labels[context.data];
                    },
                    color: '#FFFFFF'
                }
            },
            title: {
                display: true,
                text: "Ilość rozwiązanych egzaminów: " + importExamCount
            }
        }
});

var graphChart = new Chart("graph", {
    type: "bar",
    data: {
        labels: importGraphDates,
        datasets: [{
            label: 'Ostatnie wyniki',
        fill: false,
        backgroundColor: "rgba(0,0,255,1.0)",
        borderColor: "rgba(0,0,255,0.1)",
        data: importGraphPoints,
        scaleFontColor: "#FFFFFF"
        }]
    },
    options: {
        plugins: {
            datalabels: {
                formatter: function(value, context) {
                    return context.chart.data.labels[context.data];
                },
                color: '#FFFFFF'
            }
        },
        responsive: true,
        legend: {display: true},
        scales: {
        yAxes: [{ticks: {min: 0, max:74, stepSize: 5}}],
        xAxes: [{
            ticks: {
            autoSkip: false,
            maxRotation: 90,
            minRotation: 90,
            color: 'black'
            }
        }],
        },
        annotation: {
            annotations: [{
            drawTime: "beforeDatasetsDraw",
            type: "box",
            xScaleID: "x-axis-0",
            yScaleID: "y-axis-0",
            borderWidth: 0,
            yMin: 68,
            yMax: 74,
            backgroundColor: "rgba(46, 204, 113,0.3)"
            }]
        }
    }
});

function updatePieChart(time){
    $.ajax({
        url: 'pie-chart?time=' + time.value + '&category=' + document.getElementById("statisticsCategory").value,
        type: "GET",
        dataType: "json",
        success: (data) => {
            pieChart.options.title.text = "Ilość rozwiązanych egzaminów: " + data.examCount;
            pieChart.data.datasets[0].data = [data.passed, data.failed]
            pieChart.update();
        },
        error: (error) => {
            if(error.status == 400){
                window.location.href = 'login';
            }
        }
    });
}

function changeCategory(category){
    updatePieChart(document.getElementById("statisticsRange"))
    $.ajax({
        url: 'graph-chart?category=' + category.value,
        type: "GET",
        dataType: "json",
        success: (data) => {
            graphChart.data.datasets[0].data = data.graphPoints
            graphChart.data.labels = data.graphDate
            graphChart.update();
        },
        error: (error) => {
            if(error.status == 400){
                window.location.href = 'login';
            }
        }
    });
}
