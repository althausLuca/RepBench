from RepBenchWeb.models import TaskData
import time

from RepBenchWeb.utils.encoder import RepBenchJsonRespone


class TaskView:
    data_type = "abstract_task"



    @classmethod
    def specific_task(cls, request,task_id):
        """ runs asynchronous task and returns JsonResponse with task_id"""
        raise NotImplementedError("This is an abstract class")

    @classmethod
    def init_task(cls,request):
        print("init task")
        task_id = request.POST.get("task_id",False) or  request.POST.get("csrfmiddlewaretoken")

        try:  # clear older task running with same id
            TaskData.objects.get(task_id=task_id).delete()
        except TaskData.DoesNotExist:
            pass
        print("deleted old task")

        task_data = TaskData(task_id=task_id, data_type=cls.data_type)
        task_data.save()
        print("created task")
        return cls.specific_task(request, task_id)

    @staticmethod
    def fetch_data(request):
        task_id = request.POST.get("task_id",False) or  request.POST.get("csrfmiddlewaretoken")

        for i in range(25): #check that object is already created before directly running into an error
            if TaskData.objects.filter(task_id=task_id).exists():
                break
            else:
                time.sleep(0.3)

        task_data = TaskData.objects.filter(task_id=task_id).last()
        data = task_data.get_data()
        status = task_data.status
        if task_data.is_running():
            return RepBenchJsonRespone({"data": data, "status": status})
        if task_data.is_done():
            # task_data.get_recommendation("test")
            return RepBenchJsonRespone({"data": data, "status": status})

    @staticmethod
    def extract_from_task_data(task_id):
        task = TaskData.objects.get(id=task_id)
        return task
