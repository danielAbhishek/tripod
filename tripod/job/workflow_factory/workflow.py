"""
Representation of the creation of the whole set of works and related tasks,
based on the workflow that defined for the job.
"""
from datetime import timedelta

from settings.models import WorkTemplate

from job.workflow_factory.works import (
    SimpleToDo,
    EmailToDo
)


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
        self.workflow = job.workflow
        self.job_date = job.created_at
        self.data_objs = WorkTemplate.objects.filter(workflow=self.workflow)

    def create_work_and_tasks(self):
        """
        looping thru the defined work structure for the specific workflow
        and passing the information to the work creation classes, so works and
        tasks will be automatically created
        """
        for obj in self.data_objs:
            # creating instance using string value from db
            work_class = eval(obj.class_object)

            # initiating and setting to create db objects of work, task
            work_instance = work_class(
                name=obj.name,
                user=self.user,
                job=self.job
            )
            work_instance.set_data(
                description=obj.description,
                due_date=self.job_date + timedelta(days=obj.day_delta),
                work_order=obj.step_number,
                completed=True if obj.auto_complete else False
            )
            work_instance.create_db_object()

            # to-do handle this part properly
            if obj.class_object == 'SimpleToDo':
                work_instance.add_tasks()
            else:
                work_instance.add_tasks(obj.email_template)

            # delete the instance
            del work_instance
        return self
