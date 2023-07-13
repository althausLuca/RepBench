import itertools

from testing_frame_work.parser_init import init_parser
from testing_frame_work.scenarios.scen_generator import build_scenario
from testing_frame_work.scenarios.scenario import Scenario
import testing_frame_work.argument_parsers as arg_parser
import testing_frame_work.repair as alg_runner
from testing_frame_work.data_methods.data_class import infer_data_file
import injection.injection_config as ic
import testing_frame_work.scenarios.scenario_config as sc
from repair import algo_mapper

estimator_choices = list(algo_mapper.keys()) + ["all"]
scenario_choices = list(sc.SCENARIO_TYPES) + ["all"]
anomaly_choices = list(ic.ANOMALY_TYPES) + ["all"]

def main(input=None):
    args = init_parser(input=input,
                       estimator_choices=estimator_choices,
                       scenario_choices=scenario_choices,
                       anomaly_choices=anomaly_choices)

    algorithms = arg_parser.parse_repair_algorithms(args)

    scen_names = arg_parser.parse_scen_names(args)

    ### read data file_paths
    data_files = args.data
    import os
    test_data_dir = os.listdir("data/test")
    if "all" not in data_files:
        data_paths = []
        for file_name in data_files:
            data_paths.append(infer_data_file(file_name, folder="data" + os.sep + "test"))
    else:
        data_paths = [infer_data_file(file_name, folder="data/test") for file_name in test_data_dir]

    data_set_names = [s.split(os.sep)[-1].replace(".csv", "") for s in data_paths]
    print("running on", data_set_names)
    anomaly_types = arg_parser.parse_anomaly_types(args)
    cols = args.cols
    for (scen_name, data_name, anomaly_type) in itertools.product(scen_names, data_set_names, anomaly_types):
        if scen_name == sc.ANOMALY_SIZE and anomaly_type == ic.POINT_OUTLIER:
            print("skipping anomaly_lenght outlier scenario")
            continue
        try:
            scenario: Scenario = build_scenario(scen_name, data_name, a_type=anomaly_type, data_type="test", cols=cols)
        except Exception as e:
            print(f'Buidling {scen_name} on {data_name} with {anomaly_type} anomalies  failed')
            raise e
        repairer = alg_runner.AnomalyRepairer(1, 1)

        for name, test_part in scenario.name_container_iter:
            for repair_type in algorithms:
                print(f"running repair on {data_name}  {scen_name} with {repair_type} on {anomaly_type} anomalies")
                repair_info = repairer.repair_data_part(repair_type, test_part)
            test_part.save(folder=f"Results/DataSets/{scen_name}_{anomaly_type}_{name}")
        scenario.save(plot_repairs=True, res_name=args.rn)


if __name__ == '__main__':
    main()
