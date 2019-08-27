$(document).ready(function () {
    console.log('Testing');
    // Init disabled inputs
    var inputPath = '.profile .profile-info-container form .input-field '
    var disabledInputs = ['#website', '.btn #file-btn', '.file-path-wrapper #file-field']
    
    // Set cursor to disabled
    $(inputPath + disabledInputs[1]).css('cursor', 'not-allowed');

    $('#edit-profile-btn').click(function (e) { 
        // Prevent submit
        e.preventDefault();
        console.log('edit-profile-btn clicked');

        // Disable and hide html elements
        $(this).addClass('hide');
        for(let i=0; i < disabledInputs.length; i++) {
            $(inputPath + disabledInputs).removeAttr('disabled');
        }
        $(inputPath + disabledInputs[1]).css('cursor', 'pointer');
        $('#save-changes-btn').removeClass('hide');
    });

    $('.profile .profile-info-container form #save-changes-btn').click(function (e) { 
        console.log('save-changes-btn clicked');
        // Prevent submitting
        e.preventDefault();

        $(this).addClass('hide');
        for(let i=0; i < disabledInputs.length; i++) {
            $(inputPath + disabledInputs).attr('disabled', '');
        }
        $(inputPath + disabledInputs[1]).css('cursor', 'not-allowed');
        $('#edit-profile-btn').removeClass('hide');

        // Get inputs then post
        var username = $(this).attr('data-user');
        var website = $(inputPath + disabledInputs[0]).val();
        var picture = $(inputPath + disabledInputs[2]).val();
        console.log(website, picture);
        
        // $.ajax({
        //     type: "POST",
        //     url: ".",
        //     data: {
        //         website: website,
        //         picture: picture,
        //     },
        //     dataType: "json",
        //     success: function (response) {
        //         console.log(response);
                   
        //     }
        // });

        $.post('.',
            {
                website: website,
                picture: picture
            },
                function(data) {
                console.log(data);
                
            });

        // M.toast({
        //     html: 'Saved',
        //     classes: 'rounded',
        //     displayLength: 3000
        // });
    });
});