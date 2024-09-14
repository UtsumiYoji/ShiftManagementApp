$(document).ready(function() {
    // Get the URL search parameters
    var url = new URL(window.location.href);
    var params = url.searchParams;

    // Get the value of the 'disabled' query parameter (if it exists)
    var disabled = params.get('disabled');

    // Check if 'disabled' is null
    if (params.has('disabled')) {
        // Set the value of the form select element
        $('.form-select').val(disabled);
    } else {
        // Set default value
        url.searchParams.set('disabled', "False");
        window.location.href = url.toString();
    }
});

$('.form-select').change(function() {
    var val = $(this).val();
    
    var url = new URL(window.location.href);
    url.searchParams.set('disabled', val);
    window.location.href = url.toString();
});
