from RepBenchWeb.ts_manager.HighchartsMapper import map_repair_data
from repair.parameterization import BayesianOptimizer
from repair.algorithm_mapper import algo_mapper
from testing_frame_work.repair import AnomalyRepairer
import multiprocessing


def run_optimization_task(estimator, repair_inputs, param_ranges, error_loss, n_calls, n_initial_points, output_queue):
    def store_results(data):
        output_queue.put(data)

    optimizer = BayesianOptimizer(estimator, error_score=error_loss, n_calls=n_calls,
                                  n_initial_points=n_initial_points,
                                  n_restarts_optimizer=1,
                                  callback=store_results,
                                  n_jobs=1
                                  )

    params, scores = optimizer.search(repair_inputs, param_ranges,
                                      return_full_results=True)


def run_optimization(*, alg_type, n_calls, n_initial_points, injected_data_container, param_ranges, error_loss):
    estimator = algo_mapper[alg_type]()

    out_put_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=run_optimization_task, args=(estimator, { k:v.copy() for k,v in injected_data_container.repair_inputs.items()},
                                                                    param_ranges.copy(), error_loss, n_calls,
                                                                    n_initial_points,out_put_queue))
    p.start()

    import time
    return p, out_put_queue , time.time()
