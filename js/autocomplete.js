$(document).ready(function() {
    $("#search_term").autocomplete({
        source: function(request, response) {
            $.getJSON("./get_autocomplete_terms.cgi?search_term=" + request.term, function(data) {
                response($.map(data, function (value, key) {
                    return {
                        value
                    };
                }));
            });
        },
        minLength: 1,
    });
});
