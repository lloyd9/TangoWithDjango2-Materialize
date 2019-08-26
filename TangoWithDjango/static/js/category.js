$(document).ready(function () {
    $('#add-category-page').click(function(e) {
        var catname= $(this).attr('data-catname');
        var catid = $(this).attr('data-catid');
        var url = $(this).attr('data-url');
        var title = $(this).attr('data-title');
        console.log(catname, catid, url, title)
        var me = $(this)
        $.get('/rango/add/',
            {
                category_id: catid,
                url: url,
                title: title
            },
            function(data) {
                console.log(data);
                $('#pages').html(data);
                me.hide();
                M.toast({
                    html: title + ' is added in category ' + catname,
                    classes: 'rounded',
                    displayLength: 5000
                });
            });
    });
});