from celery import shared_task

from repair import Estimator, algo_mapper


@shared_task(bind=True)
def succesive_halving_task(self, alg_name, param_grid , opt_config, * , injected, truth, labels, injected_columns,my_task_id):
    from RepBenchWeb.models import TaskData
    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)
    from repair.parameterization.optimizers import SuccessiveHalvingOptimizer

    def sucessive_halving_call_back(counter,
                                    param_combinations,
                                    data_size,
                                    params_error,
                                    avg_error,
                                    kept_param_combinations,
                                    end_results=None,
                                    end_score=None):
        if end_results is not None:
            # print("Final parameters: ", end_results)
            print("Final score: ", end_score)

        # print("---------------------------------------------------")
        # store everything inside a dict:
        results = {
            "iter": counter,
            "param_combinations": param_combinations,
            "data_size": data_size,
            "params_error": params_error,
            "avg_error": avg_error,
            "kept_param_combinations": kept_param_combinations,
            "parameters": end_results,
            "score": end_score,
            "algorithm" :  alg_name

        }
        task_data.add_data(results)
        return results

    alg: Estimator = algo_mapper[alg_name]()

    optimizer = SuccessiveHalvingOptimizer(alg, "rmse", callback=sucessive_halving_call_back)

    repair_inputs = {"injected": injected,
                     "truth": truth,
                     "labels": labels,
                     "columns_to_repair": injected_columns
                     }
    optimizer.search(repair_inputs,param_grid)
    task_data.set_done()
    return "Done"
