"use strict";

var FaqPage = function () {

    var switchFaqContent = function (event, show_id, hide_ids) {
        event.preventDefault();
        hide_ids.forEach(id => $('#' + id).hide());
        $('#' + show_id).show();
    }

    // private
    var init = function () {
        var hideIds = ['faq_general_content', 'faq_account_content', 'faq_dataset_content', 'faq_detection_content', 'faq_injection_content', 'faq_recommendation_content'];

        $('#general_link').on('click', function (e) {
            switchFaqContent(e, 'faq_general_content', hideIds);
        });
        $('#dataset_link').on('click', function (e) {
            switchFaqContent(e, 'faq_dataset_content', hideIds);
        });
        $('#detection_link').on('click', function (e) {
            switchFaqContent(e, 'faq_detection_content', hideIds);
        });
        $('#injection_link').on('click', function (e) {
            switchFaqContent(e, 'faq_injection_content', hideIds);
        });
        $('#recommendation_link').on('click', function (e) {
            switchFaqContent(e, 'faq_recommendation_content', hideIds);
        });

    }
    return {
        // public
        init: function() {
            init();
        }
    };
}();