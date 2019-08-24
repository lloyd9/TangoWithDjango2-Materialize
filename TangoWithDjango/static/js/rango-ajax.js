$(document).ready(function () {
    $('#likes').click(function (e) { 
        var catid = $(this).attr('data-catid');
        $.get('/rango/like/', {category_id: catid}, function(data) {
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });

    $('#suggestion').keyup(function() {
        var query = $(this).val();
        // Send query as suggestion into the views, then get the returned data from views as data
        // The data would be the cats template, which was rendered in the views
        $.get('/rango/suggest/', {suggestion: query}, function(data) {
            $('#cats').html(data);
        });
    });

    $('.rango-add').click(function() {
        var catid = $(this).attr('data-catid');
        var url = $(this).attr('data-url');
        var title = $(this).attr('data-title');
        var me = $(this)
        $.get(
            '/rango/add/',
            {
                category_id: catid,
                url: url,
                title: title
            },
            function(data) {
                $('#pages').html(data);
                me.hide();
            });
    });
});