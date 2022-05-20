"""
Representation of the creation of the whole set of works and related tasks,
based on the workflow that defined for the job.
"""
from datetime import timedelta

from settings.models import WorkTemplate, WorkType

from job.workflow_factory.works import SimpleWork
from job.utils import update_work_completion_for_job


class WorkFlowBase:
    """
    Representation of the class which handles the work and task creation
    based on the job's workflow

    After instance has been created, call the create_work_and_tasks
    which will get the job done :-)

    * user -> user who creates
    * job -> job that created, and work and tasks needed to be created
    * workflow -> job's workflow
    * job_data -> job's created_at
    * wt_objs -> get data from WorkTemplate (a model that holds
    the basic structural information of the works that comes under
    specif workflow) that is relavent to the workflow
    """

    def __init__(self, user, job):
        self.user = user
        self.job = job
        self.job_status = True if self.job.status == 'job' else False
        self.workflow = job.workflow
        self.job_date = job.created_at
        self.work_types = WorkType.objects.all()
        self.wt_objs = WorkTemplate.objects.filter(workflow=self.workflow)

    def create_work_and_tasks(self):
        """
        looping thru the defined work structure for the specific workflow
        and passing the information to the work creation classes, so works and
        tasks will be automatically created
        """
        if self.workflow is None:
            raise Exception("workflow is not available")
        for work_type in self.work_types:
            # creating work database objects
            work_instance = SimpleWork(user=self.user,
                                       job=self.job,
                                       work_type=work_type)
            work_instance.create_db_object()
            wt_objs = self.wt_objs.filter(work_type=work_type)
            # mapping task creation to each object of work template
            work_instance.tasks = list(map(work_instance.task_factory,
                                           wt_objs))

        update_work_completion_for_job(self.job)
        self.job.save()
