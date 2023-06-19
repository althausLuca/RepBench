import injection.injection_config as ic
from testing_frame_work.parser_init import init_parser
import repair.algorithms_config as algc
import injection.injection_config as at


repair_estimators = algc.ALGORITHM_TYPES
estimator_choices = list(repair_estimators) + ["all"]

scenarios = [ic.ANOMALY_SIZE, ic.CTS_NBR , ic.ANOMALY_RATE, ic.TS_LENGTH, ic.TS_NBR , ic.ANOMALY_FACTOR]
scenario_choices = scenarios + ["all"]

anomaly_choices = list(at.ANOMALY_TYPES) + ["all"]

error_scores = ["rmse_full","rmse_partial","mae","mutual_info"]


def init_checked_parser(input):
    args = init_parser(input=input,
                       estimator_choices=estimator_choices,
                       scenario_choices=scenario_choices,
                       anomaly_choices=anomaly_choices)

    return args

def parse_scen_names(args):
    scen_params = args.scen
    scen_names = scenarios if "all" in scen_params else scen_params
    return scen_names

def parse_repair_algorithms(args):
    if "all" in args.alg:
        return algc.ALGORITHM_TYPES
    return args.alg



def parse_anomaly_types(args):
    anomaly_types_argument = args.a
    all_anomalies = at.ANOMALY_TYPES

    if "all" in anomaly_types_argument:
        return all_anomalies

    for a_type_arg in anomaly_types_argument:
        assert a_type_arg in all_anomalies, f"{a_type_arg} not in {all_anomalies}"

    return all_anomalies

