import numpy as np
from django.shortcuts import render
import json

from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from RepBenchWeb.views.config import *
from injection.injectedDataContainer import InjectedDataContainer
from repair.Dimensionality_Reduction.dimensionality_reduction_estimator import DimensionalityReductionEstimator
from testing_frame_work.repair import AnomalyRepairer
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.forms.alg_param_forms import RPCAparamForm, CDparamForm
from RepBenchWeb.ts_manager.HighchartsMapper import map_repair_data, reverse_norm
from RepBenchWeb.views.dataset_views import DatasetView
from RepBenchWeb.views.repair.repair_view import RepairView, parse_param_input
from testing_frame_work.data_methods.data_class import normalize_f


class DimensionalityReductionView(RepairView):
    template = DIMENSIONALITY_REDUCTION_TEMPLATE
    ParamForms = {"RPCA": RPCAparamForm(), "CDrec": CDparamForm()}

    @staticmethod
    def repair_data(request, setname):
        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")
        threshold = post["threshold"]

        data_container = DatasetView.load_data_container(setname)
        df_norm = data_container.norm_data  # only work with normalized data
        df_original = data_container.original_data
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}

        injected_data_container: InjectedDataContainer = injected_container_None_Series(df_norm, injected_series)

        repairer = AnomalyRepairer(1, 1)
        repair_retval = repairer.repair_data_part(alg_type, injected_data_container, params)
        repair = repair_retval["repair"]
        scores = repair_retval["scores"]
        data = {"data": [{"name": RepairView.error_map[k], "y": v} for k, v in scores.items() if
                         k in RepairView.error_map.keys()]}
        metrics = list(scores.keys())
        alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
        scores = {"name": alg_name, "colorByPoint": "true", "data": data}

        original_to_injected_links = {inj_object["linkedTo"]: inj_object["id"] for inj_object in injected_series}

        repaired_series = map_repair_data(repair, injected_data_container, alg_name, original_to_injected_links,
                                          df_original)
        context = {"repaired_series": repaired_series, "scores": scores, "metrics": metrics}

        ### Extract Reduced Series
        estimator: DimensionalityReductionEstimator = repair_retval["estimator"]

        def z_score(x):
            x_abs = np.abs(x)
            x_normalized_diff = (x_abs - np.mean(x_abs)) / np.std(x_abs)

            return x_normalized_diff

        normalized_injected, _ = normalize_f(injected_data_container.injected)

        reductions = estimator.reduction_per_classification_iter

        context["reductions"] = [
            [{"name": f"{col}_red_{r_iter + 1}",
              # "linkedTo": f"{col}_red_{1}" if i != 0 else None,
              "data": list(reverse_norm(df_reduced[col], df_original[col])),
              "norm_data": list(df_reduced[col]),
              # "true_distance":  float(np.mean(np.sqrt(reverse_norm(df_reduced[col], df_original[col]) - df_original[col])))
              }
             for i, col in enumerate(df_reduced.columns) if i in injected_data_container.injected_columns]
            for r_iter, df_reduced in enumerate(reductions) if r_iter in [0, 4, 9]]

        df_reduced = reductions[-1]
        context["final_reductions"] = \
            [{"name": f"{col}reduced",
              # "linkedTo": col+"repair"+alg_name,
              "data": list(reverse_norm(df_reduced[col], df_original[col])),
              "norm_data": list(df_reduced[col])
              # "diff_norm": list(z_score(df_reduced[col] - normalized_injected[col]))
              if i in injected_data_container.injected_columns else None,
              "threshold": threshold,
              "classified": list(estimator.anomaly_matrix[:, i] * 1)
              }
             for i, col in enumerate(df_reduced.columns) if
             i in injected_data_container.injected_columns]

        Anomalies = injected_data_container.class_df.values
        classified = estimator.anomaly_matrix
        TP = np.sum(np.logical_and(classified, Anomalies))
        TN = np.sum(np.logical_and(~classified, ~Anomalies))

        FP = np.sum(classified == 1) - TP
        FN = np.sum(np.logical_and(~classified, Anomalies))
        context["TP"] = TP
        context["FP"] = FP
        context["FN"] = FN
        context["TN"] = TN

        reconstructions_per_repair_iter = estimator.reconstructions_per_repair_iter

        rgba_colors = [(245, 127, 39), (245, 226, 39), (144, 245, 39), (39, 245, 243), (39, 54, 245, 0.8)]
        rgba_converter = lambda rgb, a: f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{a})"

        def zones(class_col):
            rgb = rgba_colors.pop(0)
            rgba_colors.append(rgb)

            zones = []
            in_anomaly = False
            for i, c in enumerate(class_col):
                if c == 1 and not in_anomaly:
                    zones.append({"value": i, "dashStyle": 'dot', "color": rgba_converter(rgb, 0.4)})
                    in_anomaly = True
                elif c == 0 and in_anomaly:
                    zones.append({"value": i, "color": rgba_converter(rgb, 1)})
                    in_anomaly = False

            zones.append({"value": i, "dashStyle": 'dot', "color": rgba_converter(rgb, 0.2)})
            return zones

        context["repair_iters"] = [
            [{"name": f"{col}_repair_iter{r_iter + 1}",
              # "linkedTo": f"{col}_red_{1}" if i != 0 else None,
              "data": list(reverse_norm(df_repair[col], df_original[col])),
              "norm_data": list(df_repair[col]),
              "zones": zones(estimator.anomaly_matrix[:, i]),
              "zoneAxis": 'x',
              }
             for i, col in enumerate(df_repair.columns) if i in injected_data_container.injected_columns]
            for r_iter, df_repair in enumerate(reconstructions_per_repair_iter) if r_iter in [0, 2, 5, 9]]

        context["injected_series"] = [
            {"name": f"TS{col}_injected",
             "data": list(reverse_norm(injected_data_container.injected.iloc[:, col],
                                       data_container.original_data.iloc[:, col])),
             "norm_data": list(injected_data_container.injected.iloc[:, col]),
             "color": "rgba(255,0,0,0.5)",
             "dashStyle": 'dot'
             }
            for _, col in enumerate(injected_data_container.injected_columns)
        ]

        context["injected_diff"] = \
            [{"name": f"TS{col}_injected_diff",
              # "linkedTo": col+"repair"+alg_name,
              "data": list(z_score(list(reverse_norm(df_reduced[col], df_original[col]))-reverse_norm(injected_data_container.injected[col],
                                       data_container.original_data[col]))),

              }
             for i, col in enumerate(df_reduced.columns) if
             i in injected_data_container.injected_columns]

        return RepBenchJsonRespone(context)


def display_dim_reduction_datasets(request=None):
    context = {}
    context["datasets"] = {dataSet.title: dataSet.get_info()
                           for dataSet in InjectedContainer.objects.all() if
                           dataSet.title is not None and dataSet.title != ""}
    return render(request, DISPLAY_DIMENSIONALITY_REDUCTION_DATASETS_TEMPLATE, context=context)
