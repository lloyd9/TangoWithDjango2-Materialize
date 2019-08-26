$(document).ready(function () {
    // TODO: Pass the category name here
    $('#likes').click(function (e) { 
        var catid = $(this).attr('data-catid');
        $.get('/rango/like/', {category_id: catid}, function(data) {
            $('.like-container').html(data);
            $('#likes').addClass('disabled')
            M.toast({
                html: 'You liked ' + catid + '!',
                classes: 'rounded',
                displayLength: 3000
            });
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
});