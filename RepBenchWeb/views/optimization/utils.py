




def parse_param_input(v: str):
    """
    Args:
        p: parameter value

    Returns:
        parsed parameter value (int, float or str)
    """
    if v.isdigit():
        return int(v)
    try:
        return float(v)
    except:
        return v


def extract_opt_input(POST):
    """Extracts the optimization input from the POST request
    Args:
        POST: POST request parameter values are expected as algname-paramname-min/max

    Returns:
        algorithm str: alg_type
        param_min_max_tuples dict: {param_name: (min,max)}
    """
    algorithm = POST.get("algorithm")
    param_min_max_tuples = {}
    for k, v in dict(POST).items():
        splitted_input = k.split("-")
        if len(splitted_input) == 3:
            v = v if not isinstance(v, list) else v[0]
            v = parse_param_input(v)
            alg_name, param_name, min_or_max = splitted_input
            if alg_name == algorithm:
                if min_or_max == "min":
                    if param_name in param_min_max_tuples:
                        param_min_max_tuples[param_name] = (v, param_min_max_tuples[param_name])
                    else:  ## max already asigned so make a tuple (min,max)
                        param_min_max_tuples[param_name] = v

                else:  ## must be max
                    if param_name in param_min_max_tuples:
                        param_min_max_tuples[param_name] = (param_min_max_tuples[param_name], v)
                    else:
                        param_min_max_tuples[param_name] = v

    return algorithm, param_min_max_tuples
