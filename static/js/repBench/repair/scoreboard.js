let scoreBoardLoadeer = function () {
}
const createScoreBoard = function () {

    document.getElementById("score_container").style.display = "block";
    RoundSliders.init(2, 15, 70);

    RoundSliders.updateValue("#RMSE-slider", 0, 0,);
    // RoundSliders.setTitle("#RMSE-slider", "RMSE");
    RoundSliders.updateValue("#MAE-slider", 0, 0,);
    // RoundSliders.setTitle("#MAE-slider", "MAE");
    RoundSliders.updateValue("#RMSE-Anomaly-slider", 0,);
    // RoundSliders.setTitle("#RMSE-Anomaly-slider", "RMSE on Anomaly");
    // scoreBoardLoadeer = setDivLoading("score_container");
}
const updateScoreBoard = function (scores) {
    RoundSliders.init(2, 15, 70);

    RoundSliders.updateValue("#RMSE-slider", scores.RMSE, scores.original_scores.RMSE);
    // RoundSliders.setTitle("#RMSE-slider", "RMSE");
    RoundSliders.updateValue("#MAE-slider", scores.MAE, scores.original_scores.MAE);
    // RoundSliders.setTitle("#MAE-slider", "MAE");
    RoundSliders.updateValue("#RMSE-Anomaly-slider", scores["RMSE on Anomaly"], 4);
    // RoundSliders.setTitle("#RMSE-Anomaly-slider", "RMSE on Anomaly");
    // scoreBoardLoadeer();
}

