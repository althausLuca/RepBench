import argparse
import sys


def name_check(choices, para_name):
    """

    Args:
        choices list[str]:  list of possible choices
        para_name str:  name of the parameter

    Returns: function that checks if the input is in the choices to be used by argument parsers
    """
    def f(str):
        result = []
        for s in str.split(","):
            if choices is not None and s not in choices:
                sys.tracebacklimit = 3
                raise SystemExit(f'{s} not a possible {para_name} inputs:{choices}')
            result.append(s)
        return result
    return f




def column_type_split(para_input:str):
    if para_input == "all":
        return "all"
    try:
        return [  int(s.strip()) for s in para_input.split(",")]
    except:
        raise SystemExit(f'only comma seperated integers are allowed  inputs:{para_input}')


def add_data_arguments_to_parser(parser, data_choices):
    parser.add_argument("-data", "-d", type= name_check(data_choices , "data set"))
    parser.add_argument("-cols", "-ts", type=column_type_split, default= "0")


def add_injection_arguments_to_parser(parser ,scenario_choices ,anomaly_choices):
    parser.add_argument('-a','-a_type', type=name_check(choices=anomaly_choices, para_name="a_type") , required=True)
    parser.add_argument("-scen", "-scennario", type=name_check(choices=scenario_choices, para_name="scen")  , required=True)
    parser.add_argument("-saveinjected",  action='store_true')


def add_repair_arguments_to_parser(parser,estimator_choices):
    parser.add_argument("-alg", type=name_check(choices=estimator_choices, para_name="alg"))
    parser.add_argument("-algx", type=str)
    parser.add_argument("-rn", "-result_name" , type=str ,default=None) # subfolder to save file
    parser.add_argument("-train", "-t" , type=str ,default="off",choices=["grid", "bayesian" , "halving" , "off"])
    parser.add_argument("-train_error", "-e" , type=str ,default="full_rmse",choices=["mae", "full_rmse", "partial_rmse"])
    parser.add_argument("-run_time_n", "-rtn" , type=int ,default=1)


def init_repair_parser():
    parser = argparse.ArgumentParser()
    add_data_arguments_to_parser(parser)
    add_repair_arguments_to_parser(parser)
    return parser.parse_args()


def init_parser(input = None , estimator_choices = None ,scenario_choices = None , data_choices = None ,anomaly_choices = None):
    parser = argparse.ArgumentParser()

    add_data_arguments_to_parser(parser , data_choices = data_choices)
    add_injection_arguments_to_parser(parser,scenario_choices = scenario_choices , anomaly_choices = anomaly_choices)
    add_repair_arguments_to_parser(parser,estimator_choices = estimator_choices)

    if input is not None:
        #For running/profiling with and IDE  or simply run it in a file
        args = parser.parse_args(input.split())
    else:
        args = parser.parse_args()

    assert args.alg is not None or args.algx is not None, f"alg or algx needs to be defined"
    return args
