$(document).ready(function () {

    

    $('#login-form-submit').click(function (e) {
        e.preventDefault();
    
        const loginForm = document.getElementById("login-form");
        const loginErrorMsg = document.getElementById("login-error-msg");

        const username = loginForm.username.value;
        const password = loginForm.password.value;
        
        $.ajax({
            type: 'POST',
            url: '/login',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'username': username,
                'password': password
            }),
            success: function (res) {
                console.log(res.response)
                if (res['success']) {
                    console.log('Successful login');

                    $.ajax({
                        type: 'GET',
                        url: '/profile/' + username,
                        contentType: 'application/json;charset=UTF-8',
                        success: function (res) {
                            // console.log(res.response)
                            window.location.href = '/profile/'+username;
                        },
                        error: function () {
                            console.log('Error');
                        }
                    });

                } else {
                    loginErrorMsg.style.opacity = 1;
                }
                //location.reload();
            },
            error: function () {
                console.log('Error');
                
            }
        });
    });

    $('#submit-user').click(function () {
        
        
        $.ajax({
            type: 'POST',
            url: '/create_user',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'username': $('#user-modal').find('.user_id').val(),
                'password': $('#user-modal').find('.password').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});