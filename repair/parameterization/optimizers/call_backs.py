

def sucessive_halving_call_back(counter,
                                param_combinations,
                                data_size ,
                                params_error ,
                                avg_error,
                                kept_param_combinations,
                                end_results= None,
                                end_score = None):

    # print(f"iter_{counter} {len(param_combinations)} parameter combinations data_size {data_size}")
    # print("avg error:" , avg_error, "Parameters:" ,params_error  )
    # print("Kept parameters: " , kept_param_combinations)
    # if end_results is not None:
        # print("Final parameters: " , end_results)
        # print("Final score: " , end_score)

    # print("---------------------------------------------------")
    #store everything inside a dict:
    results = {
        "iter": counter,
        "param_combinations": param_combinations,
        "data_size": data_size,
        "params_error": params_error,
        "avg_error": avg_error,
        "kept_param_combinations": kept_param_combinations,
        "end_results": end_results,
        "end_score": end_score
    }
    return results
