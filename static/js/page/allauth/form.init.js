"use strict";

var AllAuthForm = function () {
    
    // private
    var init = function (form_id, error_msg, hasCaptcha) {
        $('#'+form_id).on('submit', function (event) {
            event.preventDefault();
            clearFormErrors(form_id);
            clearMessages();
            var csrftoken = Cookies.get('csrftoken');
            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: $(this).attr('action'),
                data: $(this).serialize(),
                type: $(this).attr('method'),
                success: function (data, status, xhr) {
                     handleRedirect(data, xhr);
                },
                error: function (data, status, xhr) {
                    if (error_msg !== undefined) {
                        printGroupedMessages(JSON.parse('[{ "message":"' + error_msg + '", "level_tag":"error"}]'));
                    } else {
                        printMessages([{'message': "Request failed"}], "error-request");
                    }

                    if (hasCaptcha === true)
                        grecaptcha.reset();
                }
            });
        });
    }

    return {
        // public
        init: function(form_id,error_msg, hasCaptcha) {
            init(form_id, error_msg, hasCaptcha);
        }
    };
}();