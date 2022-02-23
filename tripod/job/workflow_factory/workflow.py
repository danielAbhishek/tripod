"""
Representation of the creation of the whole set of works and related tasks,
based on the workflow that defined for the job.
"""
from datetime import timedelta

from settings.models import WorkTemplate, WorkType

from job.workflow_factory.works import SimpleWork


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
    * data_objs -> get data from WorkTemplate (a model that holds
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
        self.data_objs = WorkTemplate.objects.filter(workflow=self.workflow)

    def create_work_and_tasks(self):
        """
        looping thru the defined work structure for the specific workflow
        and passing the information to the work creation classes, so works and
        tasks will be automatically created
        """
        for work_type in self.work_types:

            # creating work database objects
            work_instance = SimpleWork(
                user=self.user,
                job=self.job,
                work_type=work_type
            )
            work_instance.create_db_object()

            # adding tasks under the work
            for task_work in self.data_objs.filter(work_type=work_type):
                if task_work.class_object == 'SimpleToDo':
                    work_instance.add_simpleTask(task_work)
                elif task_work.class_object == 'EmailToDo':
                    work_instance.add_emailTask(task_work, task_work.email_template)
                elif task_work.class_object == 'ContractToDo':
                    work_instance.add_contractTask(task_work, task_work.contract_templete)
