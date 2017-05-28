/**
 * Created by mengy on 2017/5/15.
 */
$(document).ready(function () {
    $.get('/api/users', function (data) {
        var i = data.length;
        while (i--){
            $('#users').append('<li>' + data[i].username + '</li>');
        }
    });
});