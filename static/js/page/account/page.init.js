"use strict";

var AccountPage = function () {

    // private
    var init = function (user_form_id, password_form_id, account_delete_form_id) {
        initAjaxFormSubmit(user_form_id, null);
        initAjaxFormSubmit(password_form_id, null);
        initAjaxFormSubmit(account_delete_form_id, null);
    }
    return {
        // public
        init: function(user_form_id, password_form_id, account_delete_form_id) {
            init(user_form_id, password_form_id, account_delete_form_id);
        }
    };
}();
