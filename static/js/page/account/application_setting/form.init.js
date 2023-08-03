"use strict";

var ApplicationSettingsForm = function () {
    
    // private
    var init = function (form_id, format) {
        $('#'+form_id).on('submit', function (event) {
            event.preventDefault();
            var url = $(this).attr('action');
            if(format !== undefined) {
                url = url + '?format=' + format;
            }
            clearFormErrors(form_id);
            clearMessages();
            var csrftoken = Cookies.get('csrftoken');
            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: url,
                data: new FormData(this),
                type: $(this).attr('method'),
                enctype: $(this).attr('enctype'),
                processData: false,
                contentType: false,
                success: function(data, status, xhr) {
                    handleRedirect(data, xhr);
                    handleMessages(data);
                },
                error: function(data, status, xhr) {
                    printMessages([{'message': "Request failed"}], "error-request");
                    handleMessages(data);
                }
            });
        });
    }

    return {
        // public
        init: function(form_id, format) {
            init(form_id, format);
        }
    };
}();