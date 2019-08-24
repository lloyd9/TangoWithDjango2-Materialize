$(document).ready(function() {
    // Do something here
    $('#about-btn').click(function() {
        alert('You clicked the button using JQuery!');
    });

    $('#about-btn').hover(function () {
        $(this).removeClass('btn-primary').addClass('btn-success');
    }, function () {
        $(this).removeClass('btn-success').addClass('btn-primary');
    });

    $('.hover-me').hover(function() {
        $(this).css('color', 'red');
    }, function() {
        $(this).css('color', 'black');
    });
});