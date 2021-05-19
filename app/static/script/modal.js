$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#url-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const short_url = button.data('source') // Extract info from data-* attributes
        const long_url = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (short_url === 'New Url') {
            modal.find('.modal-title').text(short_url)
            $('#url-form-display').removeAttr('shortUrl')
        } else {
            modal.find('.modal-title').text('Edit Url ' + short_url)
            $('#url-form-display').attr('shortUrl', short_url)
        }

        if (long_url) {
            modal.find('.form-control').val(long_url);
        } else {
            modal.find('.form-control').val('');
        }
    })


    $('#submit-url').click(function (event) {
        const button = $(event.currentTarget);
        const short_url = $('#url-form-display').attr('shortUrl');
        const username = button.data('source');
        console.log($('#url-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: short_url ? '/edit_url/' + short_url : '/create_url/',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'long_url': $('#url-modal').find('.form-control').val(),
                'username': username 
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

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/remove_url/' + remove.data('source'),
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