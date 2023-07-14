from celery import shared_task
from repair import Estimator, algo_mapper


@shared_task(bind=True)
def bayesian_optimization_task(self, alg_name, param_grid, opt_config, *, injected, truth, labels, injected_columns, my_task_id):
    from RepBenchWeb.models import TaskData
    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)
    from repair.parameterization.optimizers import BayesianOptimizer

    def bayesian_optimization_call_back(results):
        """
        Arguments:
            results is a dict with the following structure:
                {'params': {'classification_truncation': 1, 'threshold': 0.28}, 'score': 0.52, 'iter': 15}

        """
        results["algorithm"] = alg_name
        task_data.add_data(results)

    alg: Estimator = algo_mapper[alg_name]()
    optimizer = BayesianOptimizer(alg, **opt_config ,callback=bayesian_optimization_call_back)

    repair_inputs = {"injected": injected,
                     "truth": truth,
                     "labels": labels,
                     "columns_to_repair": injected_columns
                     }

    final_parameters = optimizer.search(repair_inputs, param_grid)

    final_results = { "params": final_parameters , "algorithm" : alg_name }
    task_data.add_data(final_results)
    task_data.set_done()
    return "Done"
