$(document).ready(function() {
    
    jQuery.curCSS = jQuery.css;

    $('#id_search').autocomplete({
        source: '/blog/autocomplete/search/',
        autoFocus: true,
    });

});