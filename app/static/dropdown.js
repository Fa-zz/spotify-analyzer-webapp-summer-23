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
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});
