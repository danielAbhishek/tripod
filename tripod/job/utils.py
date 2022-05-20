from job.models import Work


def get_job_tasks(job):
    """
   return all the tasks for job
   """
    works = Work.objects.filter(job=job)
    tasks = []
    for work in works:
        [tasks.append(task) for task in work.task_set.all()]
    return tasks


def update_work_completion_for_job(job):
    works = job.work_set.all()
    for work in works:
        work.work_completion_update()
    job.save()


def tasks_completed_percentage(tasks):
    """
   return tasks completed percenage by
   taking list of tasks
   """
    total_tasks = len(tasks)
    try:
        completed_tasks = len([t for t in tasks if t.completed])
        result = (completed_tasks / total_tasks) * 100
    except ZeroDivisionError:
        result = 0
    return result


def get_job_completed_percentage(job):
    """
   return the completed job percentage
   """
    tasks = get_job_tasks(job)
    return tasks_completed_percentage(tasks)


def work_completed_percentage(work):
    """
   returning the completed work percentage
   """
    tasks = work.task_set.all()
    if tasks_completed_percentage(tasks) == 100:
        work.completed = True
        work.save()
    return tasks_completed_percentage(tasks)
