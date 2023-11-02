function usernameCheck() {
    var value = document.getElementById('id_username').value;
    var exists_error = document.getElementById('exists_error');

    $.ajax ({
        url: "check_username",
        data: {'username': value},
        type: 'get',
        datatype: 'json',
        success: function(data) {
            if (data['result']  == "fail") {
                exists_error.style.display = 'none';
                console.log('fail');
            }
            else {
                exists_error.style.display = 'block';
                console.log('sucess');
            }
        }
    });

}