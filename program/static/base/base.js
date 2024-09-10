$(document).ready(function() {
    // Get the URL search parameters
    var url = new URL(window.location.href);
    var params = url.searchParams;

    // Get the value of the 'access' query parameter (if it exists)
    var access = params.get('access');

    // Check if 'access' is 'denied'
    if (access === 'denied') {
        // Remove the 'access' query parameter and update the URL
        params.delete('access');
        history.replaceState(null, '', url.pathname);

        // Display an alert message
        $('#access-denied-modal').modal('show');
    }
});
