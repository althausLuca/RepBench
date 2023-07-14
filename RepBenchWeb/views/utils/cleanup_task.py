import time

from background_task import background
from django.core.cache import cache
import os, signal
import atexit

flaml_processes_queues_and_times = {}
optimization_processes_queue_and_times = {}


# @background(schedule=1)
def cleanup_process(token):
    clean_up(token)


def kill_process(process):
    process.terminate()
    time.sleep(2)
    if process.is_alive():
        os.kill(process.pid, 9)
    # Join the process to ensure it has finished executing
    process.join()
    assert not process.is_alive()

def clean_up(token):
    flaml_process, out_put_queue, start_time = flaml_processes_queues_and_times[token]
    flaml_process.terminate()
    flaml_process.join()
    try:
        flaml_processes_queues_and_times.pop(token, "")
    except Exception:
        pass


import psutil
@atexit.register
def clean_up_all():
    import multiprocessing
    for process in multiprocessing.active_children():
        try:
            kill_process(process)
        except Exception:
            pass
    print("cleaning up process")
    assert len(multiprocessing.active_children()) == 0

    all_processes = psutil.process_iter(['pid', 'name', 'username'])
    for process_info in all_processes:
        if process_info.info['name'] == 'python':
            print(process_info.info)

from django.core.cache import cache


def to_many_requests_response(token):
    if token in cache:
        return True
    cache.add(token, True, timeout=1)
    return False
