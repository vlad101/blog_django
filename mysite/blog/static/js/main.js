window.ga = function () { ga.q.push(arguments) }; ga.q = []; ga.l = +new Date;
ga('create', 'UA-XXXXX-Y', 'auto'); ga('set', 'anonymizeIp', true); ga('set', 'transport', 'beacon'); ga('send', 'pageview')

$(document).ready(function() {

    var editCommentModalStr = "EditCommentModal";

    // Load comment form
    $("*[id^='comment_edit_']").on('click', function(e){
        e.preventDefault();
        var commentId = $(this).attr('id').replace(/[^0-9]/g,'');
        // add comment id class
        $('#' + editCommentModalStr).addClass('comment_id_' + commentId);
        $.ajax({
            url: '/blog/comment/' + commentId,
            dataType: 'json',
            success: function (data, textStatus, jqXHR) {
                $('#' + editCommentModalStr).html(data).modal('show');
            },
            error: function (textStatus, errorThrown) {},
        });
    })

    // Edit comment
    $('#' + editCommentModalStr).submit(function(e){
        e.preventDefault();
        var commentData = $('#' + editCommentModalStr).serialize();
        var commentId = $(this).attr('class').replace(/[^0-9]/g,'');
        // remove comment id class
        $(this).removeClass('comment_id_' + commentId);
        // get comment form data
        var editCommentFormArr = objectifyForm($('#' + editCommentModalStr).serializeArray());
        var updateCommentName = (editCommentFormArr['name'] !== undefined) ? editCommentFormArr.name : null;
        var updateCommentBody = (editCommentFormArr['body'] !== undefined) ? editCommentFormArr.body : null;
        // post update comment
        $.ajax({
            headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()},
            type: "POST",
            url: "/blog/comment/edit/" + commentId,
            data: commentData,
            success: function(data, textStatus, jqXHR){
                // update data
                if(updateCommentName != null && updateCommentBody != null) {
                    if(data.hasOwnProperty('success') && data.success) {
                        $('#comment_name_' + commentId).text(' ' + updateCommentName);
                        $('#comment_body_' + commentId).text(' ' + updateCommentBody);
                    }
                }
                $('#' + editCommentModalStr).modal('hide');
            },
            error: function (textStatus, errorThrown) {
                $('#' + editCommentModalStr).modal('hide');
            },
        });
    })

});