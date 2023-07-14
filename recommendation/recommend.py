from flaml import AutoML
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/reccomendation.py

from repair import algo_mapper
from repair import get_algorithm_params
from injection.injectedDataContainer import InjectedDataContainer

from repair.algorithms_config import CDREP, RPCA, IMR, SCREEN
from recommendation.feature_extraction.feature_extraction import extract_features
from recommendation.utils.file_parsers import load_estimator

alg_names = [CDREP, RPCA, IMR, SCREEN]
autoML_file_name_default = "flaml_classifier_accuracy_time_6_non_normalized"


def get_recommendation(injected_data_container: InjectedDataContainer, classifier):
    features = extract_features(injected_data_container.injected, injected_data_container.injected_columns[0])
    used_features = classifier.feature_names_in_

    fd = pd.DataFrame.from_dict({f_name: [v] for f_name, v in features.items() if f_name in used_features})

    probabilities = classifier.predict_proba(fd).flatten()
    recommended_algorithm = classifier.predict(fd).flatten()

    from recommendation.encoder import decode
    recommended_algorithm = decode(recommended_algorithm)
    labels = classifier.classes_
    probabilities = {decode(label): p for label, p in zip(labels, probabilities)}

    results = {
        "best_estimator": recommended_algorithm,
        "recommended_algorithm": recommended_algorithm,
        "probabilities": probabilities,
        "used_estimator": str(classifier.__class__.__name__.split("Estimator")[0]),
        "data_features": features
    }
    return results


def get_all_repairs(injected_data_container: InjectedDataContainer):
    alg_scores = {}
    alg_parameters = {}
    alg_repairs = {}
    for alg_name in alg_names:
        alg_constructor = algo_mapper[alg_name]
        parameters = get_algorithm_params(alg_name)
        alg_repair = alg_constructor(**parameters).repair(**injected_data_container.repair_inputs)
        alg_score = alg_constructor(**parameters).scores(**injected_data_container.repair_inputs, predicted=alg_repair)
        alg_score.pop("rmse_per_col", None)
        alg_score.pop("original_RMSE", None)

        alg_parameters[alg_name] = parameters
        alg_scores[alg_name] = alg_score
        alg_repairs[alg_name] = alg_repair

    result = {
        "alg_repairs": alg_repairs,
        "alg_scores": alg_scores,
        "alg_parameters": alg_parameters,
    }
    return result


def get_recommendation_and_repair(injected_data_container: InjectedDataContainer, classifier, features=None):
    if True is None:
        results: dict = get_recommendation_from_classifier(injected_data_container, classifier)
    else:
        results = get_recommendation_from_classifier_and_features(classifier,
                                                                  features,
                                                                  injected_data_container.injected_columns_names)

    results.update(get_all_repairs(injected_data_container))
    return results


def get_recommendation_from_classifier_and_features(classifier, features_per_col, injected_columns):
    assert all([col in features_per_col for col in injected_columns]), \
        f"Column features columns:{injected_columns} features:{features_per_col.keys()}"

    try:
        used_features = classifier.feature_names_in_
    except:
        used_features = classifier.feature_name_  ##some classifiers have feature_name_ instead of features_names_in_

    from recommendation.encoder import decode
    try:
        used_estimator = classifier.best_estimator
    except:
        used_estimator = str(classifier.__class__.__name__.split("Estimator")[0])


    probabilities_per_col = []
    for col in injected_columns:
        features = features_per_col[col]
        not_computed_features = set(used_features).difference(set(features.keys()))
        print("missing features:",not_computed_features)
        if len(not_computed_features) > 0:
            features.update({f_name: 0 for f_name in not_computed_features})

        fd = pd.DataFrame.from_dict({f_name: [v] for f_name, v in features.items() if f_name in used_features})

        # prediction = classifier.predict(fd)[0]
        proba = classifier.predict_proba(fd)[0]

        probabilities = {str(decode(i)): p for i, p in enumerate(proba)}
        probabilities_per_col.append(probabilities)

    ##average probabilities
    probabilities = {alg_name:
                         sum([p_c[alg_name] for p_c in probabilities_per_col]) / len(probabilities_per_col)
                     for alg_name in probabilities_per_col[0].keys()}

    best_algorithm = max(probabilities, key=probabilities.get)
    results = {
        "recommended_algorithm": best_algorithm,
        "probabilities": probabilities,
        "used_estimator": used_estimator,
    }

    return results


def get_recommendation_from_classifier(injected_data_container: InjectedDataContainer, classifier) -> dict:
    """
    Returns dict: {
    "recommended_algorithm" : str
    "probabilities" : dict : alg -> float
    "alg_repairs" : dict : alg -> array
    alg_score :    dict  : alg -> errors
    alg_parameters : alg -> param_dict
    "used_classifier" : str e.g lgbm
    "injected_ts" : col_n
    "data_features" : dict "feature_name" -> val
    }
    """
    features = {col_name: extract_features(injected_data_container.injected,
                                           injected_data_container.injected_columns[col_index])
                for col_name, col_index in zip(injected_data_container.injected_columns_names,
                                               injected_data_container.injected_columns)}

    return get_recommendation_from_classifier_and_features(classifier,
                                                           features,
                                                           injected_data_container.injected_columns_names)


def get_recommendation_non_containerized(anomalous_ts, *, column_for_recommendation, label_df=None,
                                         truth=None, autoML_file_name: str = autoML_file_name_default) -> dict:
    automl: AutoML = load_estimator(autoML_file_name)
    features = extract_features(anomalous_ts, column_for_recommendation)
    fd = pd.DataFrame.from_dict({k: [v] for k, v in features.items()})

    best_algorithm = automl.predict(fd)[0]
    label_inverse = automl._label_transformer.inverse_transform

    probabilities = {label_inverse([i])[0]: p for i, p in enumerate(automl.predict_proba(fd)[0])}
    used_estimator = automl.best_estimator
    results = {
        "recommended_algorithm": best_algorithm,
        "probabilities": probabilities,
        "used_estimator": used_estimator,
        "data_features": features
    }

    alg_repairs = {}
    for alg_name in alg_names:
        if not (label_df is None and alg_name == IMR):
            alg_constructor = algo_mapper[alg_name]
            parameters = get_algorithm_params(alg_name)
            alg_repair = alg_constructor(**parameters).repair(anomalous_ts, truth=None,
                                                              columns_to_repair=[column_for_recommendation],
                                                              labels=label_df)
            alg_repairs[alg_name] = alg_repair

    if label_df is None:
        # filter out IMR
        p_imr = probabilities.pop(IMR)
        resulting_probability = 1 - p_imr
        probabilities = {k: v / resulting_probability for k, v in probabilities.items()}
        best_algorithm = max(probabilities, key=probabilities.get)
        results["recommended_algorithm"] = best_algorithm
        results["probabilities"] = probabilities

    results["alg_repairs"] = alg_repairs

    return results
