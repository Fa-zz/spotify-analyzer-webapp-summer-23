function getVar(vars) {
    return vars
}

$(document).ready(function() {
    $('#dd-type, #dd-time-frame, #dd-sort').change(function() {
        const ddType = $('#dd-type').val();
        const ddTimeFrame = $('#dd-time-frame').val();
        const ddSort = $('#dd-sort').val();

        const url = $('#dd-vars').data('url');

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                dd_type: ddType,
                dd_time_frame: ddTimeFrame,
                dd_sort: ddSort,
            },
            success: function(data) {
                $('#content').html(data.content);
                displayGraph = data.displayGraph;
                var genreList = data.genreList;
                var genreCounts = data.genreCounts;
                var genreColors = data.genreColors;
                console.log(displayGraph, genreList, genreCounts, genreColors);

                // Only create the chart if displayGraph is true
                if (displayGraph) {
                    var chartData = {
                        labels: genreList,
                        datasets: [{
                            label: '# of artists',
                            backgroundColor: genreColors,
//                            borderColor: 'black',
//                            borderWidth: 1,
                            data: genreCounts,
                            hoverOffset: 5
//                            barPercentage: 1, // Adjust the bar width here
//                            categoryPercentage: 1 // Adjust the category width here
                        }]
                    };

                    const ctx = document.getElementById('pie-chart').getContext('2d');

                    // Check if a chart instance exists for the canvas
                    const existingChart = Chart.getChart(ctx);
                    if (existingChart) {
                        existingChart.destroy(); // Destroy the existing chart
                    }

                    var chartId = new Chart(ctx, {
                        type: 'pie',
                        data: chartData,
                        options: {
                            responsive: false,
                            plugins: {
                                legend: {
                                    display: true,
                                },
                                tooltip: {
                                    titleFontSize: 16, // Adjust the title font size
                                    bodyFontSize: 14, // Adjust the body font size
                                }
                            }
                        },
                    });
                }
            },
        });
    });
});