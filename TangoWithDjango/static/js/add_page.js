$(document).ready(function () {
    $('.add-page-manually .form-container .row .col #page_form .add-page-manually-btn').click(function (e) { 
        // e.preventDefault();
        var catName = $(this).attr('data-catname');
        M.toast({
            html: 'Page Added to ' + catName,
            classes: 'rounded',
            displayLength: 3000
        });
    });
});