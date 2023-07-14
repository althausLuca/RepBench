from celery import shared_task

import os
import shutil
from datetime import datetime, timedelta

# logger = logging.getLogger(__name__)


def revoke_task(task_id):
    from celery.contrib.abortable import AbortableAsyncResult
    task = AbortableAsyncResult(task_id)
    task.abort()
    task.revoke(terminate=True)


@shared_task
def remove_ray_files(minutes=10):
    """
    Remove files older than 10 minutes from ray_tunes

    manual file removal:
    sudo docker ps # to obtain celery_container_id
    sudo docker exec -it celery_container_id  /bin/bash
    cd ~/ray_results
    ...
    """
    folder_paths = [os.path.expanduser("~/ray_results"),os.path.expanduser("/tmp/ray")]
    for folder_path in folder_paths:
        threshold = datetime.now() - timedelta(minutes=minutes)

        # List all files in the folder
        files = os.listdir(folder_path)
        # Iterate over the files and delete those older than the threshold
        for file_name in files:
            try:
                file_path = os.path.join(folder_path, file_name)
                # modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_name != "session_latest":
                    shutil.rmtree(file_path)
                else:
                    pass
            except Exception as e:
                print(f"Failed to delete file: {file_name} due to: {e}")