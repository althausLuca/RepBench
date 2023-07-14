from injection.injectedDataContainer import InjectedDataContainer
from repair import algo_mapper
from repair.parameterization.optimizers import BayesianOptimizer
from testing_frame_work.repair import AnomalyRepairer
from RepBenchWeb.ts_manager.HighchartsMapper import map_repair_data

job_status = {}
job_results = {}

def retrieve_results(job_id):
    data = job_results[job_id]
    if job_status[job_id] == 'running':
        return 'running', data
    elif job_status[job_id] == 'finished':
        return 'finished', data

    assert False

def add_job(job_id):
    # with open(f"web/mysite/RepBenchWeb/BenchmarkMaps/{job_id}.txt", 'w') as f:
    #     pass
    job_status[job_id] = "running"
    job_results[job_id] = []
    return job_id



    # with open(f"web/mysite/RepBenchWeb/BenchmarkMaps/{job_id}.txt", 'a') as f:
    #     f.write(str(data))


def start(job_id, param_ranges, alg_type, injected_data_container: InjectedDataContainer, *, error_loss, n_calls,
          n_initial_points):

    def save(data):
        job_results[job_id].append(data)

    def callback():
        estimator = algo_mapper[alg_type]()

        optimizer = BayesianOptimizer(estimator, error_score=error_loss, n_calls=n_calls,
                                      n_initial_points=n_initial_points,
                                      n_restarts_optimizer=1,
                                      callback=save,
                                      n_jobs=1
                                      )

        params, scores = optimizer.search(injected_data_container.repair_inputs, param_ranges,
                                          return_full_results=True,
                                          )

        min_index = list(scores).index(min(scores))
        optimal_params = params[min_index]

        repairer = AnomalyRepairer(1, 1)
        repair_info = repairer.repair_data_part(alg_type, injected_data_container, optimal_params)
        repair = repair_info["repair"]

        repaired_series = map_repair_data(repair, injected_data_container, alg_type)

        data = {"alg_type": alg_type,
                "data": [{"name": dict(param), "y": float(score)} for param, score in zip(params, scores)],
                "error_loss": error_loss,
                "n_calls": n_calls,
                "n_initial_points": n_initial_points,
                "repaired_series": repaired_series,
                "optimal_params": optimal_params
                }

        job_status[job_id] = 'finished'
        return data

    return callback





