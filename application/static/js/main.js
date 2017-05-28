/**
 * Created by mengy on 2017/5/17.
 */
$(document).ready(function () {

    $.getJSON(
        '/store',
        function (data) {
            alert(data);
        }
    );

});