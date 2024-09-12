$(document).ready(function() {
    // Get the URL search parameters
    var url = new URL(window.location.href);
    var params = url.searchParams;

    // Get the value of the 'date_left' query parameter (if it exists)
    var date_left = params.get('date_left');

    // Check if 'date_left' is null
    if (params.has('date_left')) {
        // Set the value of the form select element
        $('.form-select').val(date_left);
    } else {
        // Set default value
        url.searchParams.set('date_left', "True");
        window.location.href = url.toString();
    }
});

$('.form-select').change(function() {
    var val = $(this).val();
    
    var url = new URL(window.location.href);
    url.searchParams.set('date_left', val);
    window.location.href = url.toString();
});
