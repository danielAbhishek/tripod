"""
Representation of the task classes are here, and the main goal of these
implementation is to create classes which are responsible to create task
objects in database.
"""
from abc import ABC, abstractmethod

from job.workflow_factory.task_form import TaskForm


class TaskBase(ABC):
    """Basic representation of creating task"""

    @abstractmethod
    def set_data(self, description, template):
        """creating the data dictionary to pass into form"""
        pass

    @abstractmethod
    def create_db_object(self, data):
        """creating database object that will be saved"""
        pass


class ToDoTask(TaskBase):
    """
    Simple To-Do task that completes the task

    create instance with below mentioned data and then using set_data you can
    add description, template (optional). Finally call create_db_object
    to create the object in database

    * __data -> dictionary of data that passed to TaskFrom for creating db obj
    * task -> task db object; init as None type
    * name -> name of the task
    * user -> user object for update created_by
    * work -> work db class that responsible for the tasks
    """
    def __init__(self, name, user, work):
        self.__data = {}
        self.task = None
        self.name = name
        self.user = user
        self.work = work

    def set_data(self, description, template=None):
        """
        setting the data dictionary with task details which was defined at the
        object init and also adding description too, and completed is set to
        false as default and task_type is td (which is To-Do)
        """
        self.__data = {
            'task_name': self.name,
            'work': self.work,
            'description': description,
            'completed': False,
            'task_type': 'td',
        }
        return self.__data

    def create_db_object(self):
        """
        creating task db objects with data
        that passed using set_data function
        """
        form = TaskForm(
            data=self.__data, userObj=self.user, operation='creating'
        )
        if form.is_valid():
            self.task = form.save()
            return self.task
        else:
            print(form.errors)


class EmailTask(ToDoTask):
    """
    Email task which is inherited from ToDoTask class, so it has the basic
    functionality (refer ToDoTask for more information) of the ToDo
    and sending email
    * task_type is overidden as em (which is Email Task)
    * email template has to be passed additionally
    """

    def set_data(self, description, email_template):
        """setting the data dictionary with task details"""
        self.__data = super(EmailTask, self).set_data(description)
        self.__data['task_type'] = 'em'
        self.__data['email_template'] = email_template
        return self.__data
