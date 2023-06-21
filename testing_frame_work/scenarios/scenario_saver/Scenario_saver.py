import os
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
from repair.algorithms_config import ALGORITHM_COLORS
from testing_frame_work.scenarios.plotting.plotters import plot_data_part
from injection.injectedDataContainer import InjectedDataContainer
from injection.utils.label_generator import get_anomaly_ranges
from testing_frame_work.scenarios.plotting.plotters import plot_data_part
import numpy as np
from pathlib import Path
from injection.utils.label_generator import get_anomaly_ranges

#
# def save_params(scenario, path):
#     os.makedirs(path, exist_ok=True)
#     full_dict = {}
#     anomaly_percents = []
#     part: InjectedDataContainer
#     for part_name, part in scenario.part_scenarios.items():
#         full_dict[part_name] = {}
#         anomaly_percents.append(part.a_perc)
#         for repair_name, repair_dict in part.repairs.items():
#             params = repair_dict["parameters"]
#             full_dict[part_name][repair_name] = params
#
#     res_df = pd.DataFrame(full_dict).T.applymap(lambda d: ",".join([f"{k}:{v}" for k, v in d.items()]))
#     res_df.insert(0, "perc", anomaly_percents, True)
#     res_df.to_csv(f'{path}/params.txt')
#
#     ### correlation save
#     with open(f'{path}/corr.txt', 'w') as f:
#         if scenario.common_truth:
#             first, *_ = scenario.part_scenarios.values()
#             first: InjectedDataContainer
#             first.truth_corr.to_csv(f)
#             for part_name, part_scen in scenario.part_scenarios.items():
#                 f.write(str(part_name) + "\n")
#                 part_scen.injected_corr.to_csv(f)
#                 f.write("\n")
#
#         else:
#             part_scen: InjectedDataContainer
#             for part_name, part_scen in scenario.part_scenarios.items():
#                 f.write(str(part_name) + "\n")
#                 part_scen.truth_corr.to_csv(f)
#                 f.write(str(part_name) + "Injected:\n")
#                 part_scen.injected_corr.to_csv(f)
#                 f.write("\n")


def save_error(scenario, path):
    from itertools import cycle

    initial_path = path
    lines = ["solid", "dashed", "dotted", "dashdot"]
    # colors = ["red", "green", "green",  "green", "purple", "blue"]
    path = f"{path}/error"
    try:
        os.makedirs(path)
    except:
        pass
    try:
        plt.clf()
        plt.close()
    except:
        pass

    for metric, metric_df in scenario.score_dfs().items():
        error_path = f'{path}/{metric}'
        if "time" in metric:
            error_path = f'{"/".join(initial_path.split("/")[:-2])}/runtime'
        try:
            os.makedirs(error_path)
        except:
            pass

        columns = list(metric_df.columns)
        cyclers = {}
        try:
            for name_type in columns:
                color = ALGORITHM_COLORS[name_type[1]]
                if color not in cyclers:
                    cyclers[color] = cycle(lines)
                plt.plot(metric_df[name_type], marker='x', label=name_type[0], color=color, ls=next(cyclers[color]))
            plt.xlabel(metric_df.index.name)
            plt.ylabel(metric)
            lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.savefig(f'{error_path}/{metric}.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
            plt.clf()
            plt.close()
        except:
            pass
        metric_df.columns = [name for name, type in metric_df.columns]
        metric_df.to_csv(f'{error_path}/{metric}.txt')


def save_repair_plots(scenario, path):
    plt.close('all')
    for part_scen_name, part_scen in scenario.part_scenarios.items():
        plot_data_part(part_scen, path=path, file_name=f"{part_scen_name}.svg")
    plt.close('all')

    for repair_name in scenario.repair_names:
        algo_path = f'{path}/{repair_name}'

        Path(algo_path).mkdir(parents=True, exist_ok=True)

        plt.close('all')
        scenario_part: InjectedDataContainer
        for i, (part_scen_name, scenario_part) in enumerate(scenario.part_scenarios.items()):
            full_truth, full_injected = scenario_part.truth, scenario_part.injected
            cols = scenario_part.injected_columns
            klass = scenario_part.klass
            axis = plt.gca()
            axis.set_rasterization_zorder(0)
            axis.set_title(f'{part_scen_name}')
            algo_part = scenario_part.repairs[repair_name]
            full_repair = algo_part["repair"]

            for col in cols:
                col_nbr = col + 1
                a_ranges = get_anomaly_ranges(klass.iloc[:, col])
                n_ranges = min(len(a_ranges), 3)
                selected_ranges_i = list(np.random.choice(range(len(a_ranges)), size=n_ranges, replace=False))
                for a_index, range_index in enumerate(["full_range"] + selected_ranges_i):
                    if a_index == 0:
                        a_index = "fullrange"
                        start, end = 0, full_truth.shape[0] - 1
                    else:
                        range_ = a_ranges[range_index]
                        start, end = max(0, min(range_) - 20), min(full_truth.shape[0] - 1, max(range_) + 20)
                    truth = full_truth.iloc[start:end, col]
                    truth, index = truth.values, truth.index.values
                    injected = full_injected.iloc[start:end, col].values
                    repair = full_repair.iloc[start:end, col].values
                    axis.set_xlim(index[0] - 0.1, index[-1] + 0.1)
                    line, = plt.plot(index, truth)
                    lw = plt.getp(line, 'linewidth')

                    axis.set_prop_cycle(None)
                    ### repair plot

                    ###
                    mask = (injected != truth).astype(int)
                    mask[1:] += mask[:-1]
                    mask[:-1] += mask[1:]
                    mask = np.invert(mask.astype(bool))
                    masked_injected = np.ma.masked_where(mask, injected)
                    plt.plot(index, masked_injected, color="red", ls='--', marker=".", label="injected")
                    plt.plot(index, repair, lw=lw / 2, label="repair", color="blue")

                    plt.plot(index, truth, color="black", lw=lw, label="truth")
                    plt.legend()
                    axis.xaxis.set_major_locator(MaxNLocator(integer=True))
                    plt.savefig(f"{algo_path}/{scenario.scen_name}_{part_scen_name}_TS{col_nbr}_{a_index}.svg")
                    plt.close('all')
                    
                    
def save_precision(repaired_scenario , path , repair_plot ):
    path = f"{path}/precision/"
    try:
        os.makedirs(path)
    except:
        pass

    save_error(repaired_scenario,path)
    if repair_plot:
        repair_path = path + "repair"
        try:
            os.makedirs(repair_path)
        except:
            pass
        save_repair_plots(repaired_scenario,repair_path)










