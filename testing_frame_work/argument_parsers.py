import injection.injection_config as ic
import repair.algorithms_config as algc
from testing_frame_work.scenarios.scenario_config import SCENARIO_TYPES
from repair.utils import get_main_alg_name

def parse_scen_names(args):
    scen_params = args.scen
    scen_names = list(SCENARIO_TYPES) if "all" in scen_params else scen_params
    return scen_names


def parse_repair_algorithms(args):
    if "all" in args.alg:
        return algc.ALGORITHM_TYPES
    if "main" in args.alg:
        return algc.MAIN_ALGORITHMS
    algorithms = []
    print(args.alg)
    for alg_name in args.alg:
        algorithms.append(get_main_alg_name(alg_name.strip()))

    print("running on algorithms", algorithms)
    return algorithms



def parse_anomaly_types(args):
    anomaly_types_argument = args.a
    all_anomalies = ic.ANOMALY_TYPES

    if "all" in anomaly_types_argument:
        return all_anomalies

    for a_type_arg in anomaly_types_argument:
        assert a_type_arg in all_anomalies, f"{a_type_arg} not in {all_anomalies}"

    return all_anomalies
