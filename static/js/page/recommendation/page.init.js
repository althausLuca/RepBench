"use strict";

var DatasetRecommendationPage = function () {

    // private
    var init = function (dataset_json_url, dataset_download_file_url, selected_button, clear_button_id) {

        // plot
        VadetisColumnHighcharts.init("highcharts_plot_container");
        VadetisHighchartsClear.init("highcharts_plot_container", clear_button_id, function () {
            $('#recommendation_portlets').empty();
            $('#recommendation_summary_portlet').remove();
        });

        // time series
        VadetisHighcharts.init("highcharts_container", dataset_json_url, selected_button);

        VadetisHighchartsLoad.init("highcharts_container", "raw_btn", dataset_json_url, "raw", function () {});
        VadetisHighchartsLoad.init("highcharts_container", "zscore_btn", dataset_json_url, "zscore", function () {});

        VadetisHighchartsFileDownload.init("highcharts_container", "download_csv", dataset_download_file_url, "csv");
        VadetisHighchartsFileDownload.init("highcharts_container", "download_json", dataset_download_file_url, "json");

        switchColorLegend(false);
    }
    return {
        // public
        init: function(dataset_json_url, dataset_download_file_url, selected_button, clear_button_id) {
            init(dataset_json_url, dataset_download_file_url, selected_button, clear_button_id);
        }
    };
}();