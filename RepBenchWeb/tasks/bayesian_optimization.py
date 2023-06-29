from celery import shared_task

from repair import Estimator, algo_mapper


@shared_task(bind=True)
def bayesian_optimization_task(self, alg_name, param_grid, opt_config, *, injected, truth, labels, injected_columns, my_task_id):
    from RepBenchWeb.models import TaskData
    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)
    from repair.parameterization.optimizers import BayesianOptimizer

    alg: Estimator = algo_mapper[alg_name]()

    def bayesian_optimization_call_back(results):
        """
        Arguments:
            results is a dict with the following structure:
                {'params': {'classification_truncation': 1, 'threshold': 0.28}, 'score': 0.52, 'iter': 15}

        """
        print("Bayesian optimization results: ", results)
        task_data.add_data(results)
        # print("IN TASK ID", task_data.task_id)
        # print("in task data", task_data.data)

    optimizer = BayesianOptimizer(alg, "rmse", callback=bayesian_optimization_call_back)

    repair_inputs = {"injected": injected,
                     "truth": truth,
                     "labels": labels,
                     "columns_to_repair": injected_columns
                     }

    optimizer.search(repair_inputs, param_grid)

    task_data.set_done()
    return "Done"
