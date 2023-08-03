"use strict";

var AccountTrainingDatasetUploadPage = function () {

    // private
    var init = function (upload_form_id) {
        initAjaxFormSubmitWithDisable(upload_form_id, "json");
    }
    return {
        // public
        init: function(upload_form_id) {
            init(upload_form_id);
        }
    };
}();
