"""
Representation of work classes are here, which are acting as factory classes
that create instance of work db object and instance of task class based on the
criteria that passed, and they does their job to create db objects.
"""
from abc import ABC, abstractmethod

from job.workflow_factory.tasks import ToDoTask, EmailTask

from job.workflow_factory.work_form import WorkForm


class WorkBase(ABC):
    """Basic representation of creating work"""

    @abstractmethod
    def set_data(self, description, due_date, completed=False):
        """creating data dictionary to pass into form"""
        pass

    @abstractmethod
    def add_task_type(self):
        """adding the task type"""
        pass

    @abstractmethod
    def create_db_object(self, data):
        """creating database object that will get saved"""
        pass

    @abstractmethod
    def add_tasks(self, template):
        """adding the task db objects"""
        pass


class SimpleToDo(WorkBase):
    """
    Simple To Do work

    After creating the instance, by calling set_data(), additional information
    can be passed. Then calling create_db_object will save the work instance
    in the database. Following to that calling add_tasks and passing data
    (if needed) will add the relavent tasks.

    * __data -> dictionary of data that passed into workform for db object
    creation
    * name -> name of the work
    * user -> user who create
    * job -> job that will be responsible for the work
    * tasks -> list of tasks which under specific work
    * work -> created work db object; init as None
    """
    def __init__(self, name, user, job):
        self.__data = {}
        self.name = name
        self.user = user
        self.job = job
        self.tasks = []
        self.work = None

    def set_data(self, description, due_date, work_order, completed=False):
        """
        setting the data dictionary with work details
        * description -> explanation of the work
        * due_date -> due date of the specif work
        * work_order -> order of specific work among all works
        * completed -> set False as default
        """
        self.__data = {
            'work_name': self.name,
            'work_order': work_order,
            'job': self.job,
            'description': description,
            'completed': completed,
            'due_date': due_date
        }
        return self

    def add_task_type(self, task_type):
        """adding task type to the object"""
        self.__data['task_type'] = task_type

    def create_db_object(self, task_type='simple-todo'):
        """
        creating task db objects with the data passed using
        set_data function
        """
        self.add_task_type(task_type)

        # creating work db instance using form
        form = WorkForm(
            data=self.__data, userObj=self.user, operation='creating'
        )
        if form.is_valid():
            self.work = form.save()
            return self.work
        else:
            print(form.errors)

    def add_tasks(self):
        """
        automcatically created ToDoTask instance, get added to the database
        """
        name = self.name + " (adding todo task)"
        description = f"todo task {self.name} work"
        toDoTask = ToDoTask(name, self.user, self.work)
        toDoTask.set_data(description)
        toDoTask = toDoTask.create_db_object()
        self.tasks.append(toDoTask)
        return self.tasks


class EmailToDo(SimpleToDo):
    """
    inherited SimpleToDo, and overrides the task_type and the tasks creation
    """

    def create_db_object(self):
        """
        calling the super/ parent create_db_object and passing the new value
        for task_type
        """
        super(EmailToDo, self).create_db_object(task_type='email-todo')

    def add_tasks(self, template):
        """
        calling super/ parent add_tasks() to create todo task
        and also creating the email todo task as well, using the
        passed template
        """
        self.tasks = super(EmailToDo, self).add_tasks()
        name = self.name + " (sending email)"
        description = f"sending email task {self.name} work"
        emailTask = EmailTask(name, self.user, self.work)
        emailTask.set_data(description, template)
        emailTask = emailTask.create_db_object()
        self.tasks.append(emailTask)
        return self.tasks
