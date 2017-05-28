/**
 * Created by mengy on 2017/5/25.
 */
$(document).ready(function () {
    $.get({
        url: '/api/file_manager',
        success: function (data) {
            var filename_list = '';
            /* {filename: url} saved in data */
            for (var filename in data) {
                filename_list +=
                    '<li>' + filename +
                        '<button class="btn">' +
                            '<a href=' + data[filename] + '>' + 'Download' + '</a>' +
                        '</button>' +
                        '<button class="btn btn-del" data-filename=' + filename + '>' +
                            'Delete' +
                        '</button>' +
                    '</li>';
            }
            $('#uploaded-csv').append(filename_list);
        },
        complete: function () {
            $('.btn-del').on('click', function () {
                var confirmed = confirm('确认删除？');
                if (confirmed){
                    $.ajax({
                        method: 'DELETE',
                        url: '/api/file_manager',
                        data: {'filename': $(this).data('filename')},
                        success: function () {
                            alert('已删除！');
                        }
                    });
                    $(this).parent().remove();
                }
            });
        }
    });

    /*
    * 从jQuery 1.8开始，该函数只能为document对象
    * 的ajaxComplete事件绑定处理函数，
    * 为其他元素绑定的事件处理函数不会起作用。*/
    /*
    * 发现一个现象：
    * 连续删除文件时，alert() 弹出次数会翻倍，
    * 直接原因，在 ajaxComplete 函数中使用了ajax方法，
     * 避免这种情况，应该在每次ajax请求的
     * complete 回调函数中使用需要的ajax方法 */
    $(document).ajaxComplete(function () {

    });
    
});