$(document).ready(function () {
    $('#submit-registration-form').click(function (e) { 
        // e.preventDefault();
        // TODO: prevent default then check fields before posting
        M.toast({
            html: 'Choose a stronger password',
            classes: 'rounded',
            displayLength: 3000
        });
    });
});