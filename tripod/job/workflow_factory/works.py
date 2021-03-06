"""
Representation of work classes are here, which are acting as factory classes
that create instance of work db object and instance of task class based on the
criteria that passed, and they does their job to create db objects.
"""
from abc import ABC, abstractmethod

from job.workflow_factory.tasks import (ToDoTask, EmailTask, ContractTask,
                                        QuestTask, AppointmentTask)
from job.workflow_factory.forms import WorkForm


class WorkBase(ABC):
    """Basic representation of creating work"""

    @abstractmethod
    def set_data(self, description, due_date, completed=False):
        """creating data dictionary to pass into form"""
        pass

    @abstractmethod
    def create_db_object(self, data):
        """creating database object that will get saved"""
        pass


class SimpleWork(WorkBase):
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

    def __init__(self, user, job, work_type):
        self.__data = {}
        self.user = user
        self.job = job
        self.work_type = work_type
        self.tasks = []
        self.work = None
        self.task_types = {
            'ToDoTask': 'simple Task',
            'EmailTask': 'an email will be sent upon completion',
            'ContractTask': 'contract and invoice will be shared with client',
            'QuestTask': 'Questionnaire will be shared with client',
            'AppointmentTask': 'booking information will be shared with client'
        }

    def set_data(self):
        """
        setting the data dictionary with work details
        * description -> explanation of the work
        * due_date -> due date of the specif work
        * work_order -> order of specific work among all works
        * completed -> set False as default
        """
        self.__data = {
            'work_name': self.work_type.work_type,
            'work_order': self.work_type.work_order,
            'job': self.job
        }
        return self

    def create_db_object(self, task_type='simple-todo'):
        """
        creating task db objects with the data passed using
        set_data function
        """
        self.set_data()

        # creating work db instance using form
        form = WorkForm(data=self.__data,
                        userObj=self.user,
                        operation='creating')
        if form.is_valid():
            self.work = form.save()
            return self.work
        else:
            print(form.errors)

    def task_factory(self, obj):
        """creating task factory"""
        #  print(obj)
        name = obj.name
        description = f"{obj.description}\n{self.task_types[str(obj.class_object)]}"
        class_obj = eval(obj.class_object)
        task = class_obj(name, self.user, self.work)
        task.set_data(description, obj)
        task = task.create_db_object()

    # def add_simpleTask(self, obj):
    #     """
    #     automcatically created ToDoTask instance, get added to the database
    #     """
    #     name = obj.name + " (adding todo task)"
    #     description = f"todo task {name} work\n{obj.description}"
    #     toDoTask = ToDoTask(name, self.user, self.work)
    #     toDoTask.set_data(description, obj.step_number)
    #     toDoTask = toDoTask.create_db_object()
    #     self.tasks.append(toDoTask)
    #     return self.tasks
    #
    # def add_emailTask(self, obj):
    #     """
    #     creating a email sharing task
    #     """
    #     name = obj.name + " (sending email)"
    #     description = f"sending email task {name} work\n{obj.description}"
    #     emailTask = EmailTask(name, self.user, self.work)
    #     emailTask.set_data(description, obj.step_number, obj.email_template)
    #     emailTask = emailTask.create_db_object()
    #     self.tasks.append(emailTask)
    #     return self.tasks
    #
    # def add_contractTask(self, obj):
    #     """
    #     creating a contract and invoice sharing task
    #     """
    #     # self.tasks = super(ContractToDo, self).add_tasks()
    #     name = obj.name + " (sending contract)"
    #     description = f"sending contract for booking task {name} work\n{obj.description}"
    #     contractTask = ContractTask(name, self.user, self.work)
    #     contractTask.set_data(description, obj.step_number, obj.contract_templete)
    #     contractTask = contractTask.create_db_object()
    #     self.tasks.append(contractTask)
    #     return self.tasks
    #
    # def add_questTask(self, obj):
    #     """
    #     creating a questionnaire sharing task
    #     """
    #     # self.tasks = super(ContractToDo, self).add_tasks()
    #     name = obj.name + " (sending questionnaire)"
    #     description = f"sending questionnaire for booking task {name} work\n{obj.description}"
    #     questTask = QuestTask(name, self.user, self.work)
    #     questTask.set_data(description, obj.step_number, obj.quest_template)
    #     questTask = questTask.create_db_object()
    #     self.tasks.append(questTask)
    #     return self.tasks
    #
    # def add_appointmentTask(self, obj):
    #     """
    #     creating the appointment making task
    #     """
    #     # self.tasks = super(ContractToDo, self).add_tasks()
    #     name = obj.name + " (making an appointment)"
    #     description = f"making an appointment and registering {name} work\n{obj.description}"
    #     appTask = AppointmentTask(name, self.user, self.work)
    #     appTask.set_data(description, obj.step_number, obj.email_template)
    #     appTask = appTask.create_db_object()
    #     self.tasks.append(appTask)
    #     return self.tasks
    #
    # def createTasks(self, objs):
    #     """
    #     By providing the task type. and they should be available
    #     in the work template class
    #     """
    #     for obj in objs:
    #         if obj.class_object == 'SimpleToDo':
    #             self.add_simpleTask(obj)
    #         elif obj.class_object == 'EmailToDo':
    #             self.add_emailTask(obj)
    #         elif obj.class_object == 'ContractToDo':
    #             self.add_contractTask(obj)
    #         elif obj.class_object == 'QuestToDo':
    #             self.add_questTask(obj)
    #         elif obj.class_object == 'AppToDo':
    #             self.add_appointmentTask(obj)


#
#
# class SimpleToDo(WorkBase):
#     """
#     Simple To Do work
#
#     After creating the instance, by calling set_data(), additional information
#     can be passed. Then calling create_db_object will save the work instance
#     in the database. Following to that calling add_tasks and passing data
#     (if needed) will add the relavent tasks.
#
#     * __data -> dictionary of data that passed into workform for db object
#     creation
#     * name -> name of the work
#     * user -> user who create
#     * job -> job that will be responsible for the work
#     * tasks -> list of tasks which under specific work
#     * work -> created work db object; init as None
#     """
#     def __init__(self, name, user, job):
#         self.__data = {}
#         self.name = name
#         self.user = user
#         self.job = job
#         self.tasks = []
#         self.work = None
#
#     def set_data(self, description, due_date, work_order, completed=False):
#         """
#         setting the data dictionary with work details
#         * description -> explanation of the work
#         * due_date -> due date of the specif work
#         * work_order -> order of specific work among all works
#         * completed -> set False as default
#         """
#         self.__data = {
#             'work_name': self.name,
#             'work_order': work_order,
#             'job': self.job,
#             'description': description,
#             'completed': completed,
#             'due_date': due_date
#         }
#         return self
#
#     def add_task_type(self, task_type):
#         """adding task type to the object"""
#         self.__data['task_type'] = task_type
#
#     def create_db_object(self, task_type='simple-todo'):
#         """
#         creating task db objects with the data passed using
#         set_data function
#         """
#         self.add_task_type(task_type)
#
#         # creating work db instance using form
#         form = WorkForm(
#             data=self.__data, userObj=self.user, operation='creating'
#         )
#         if form.is_valid():
#             self.work = form.save()
#             return self.work
#         else:
#             print(form.errors)
#
#     def add_tasks(self):
#         """
#         automcatically created ToDoTask instance, get added to the database
#         """
#         name = self.name + " (adding todo task)"
#         description = f"todo task {self.name} work"
#         toDoTask = ToDoTask(name, self.user, self.work)
#         toDoTask.set_data(description)
#         toDoTask = toDoTask.create_db_object()
#         self.tasks.append(toDoTask)
#         return self.tasks
#
#
# class EmailToDo(SimpleToDo):
#     """
#     inherited SimpleToDo, and overrides the task_type and the tasks creation
#     """
#
#     def create_db_object(self):
#         """
#         calling the super/ parent create_db_object and passing the new value
#         for task_type
#         """
#         super(EmailToDo, self).create_db_object(task_type='email-todo')
#
#     def add_tasks(self, template):
#         """
#         calling super/ parent add_tasks() to create todo task
#         and also creating the email todo task as well, using the
#         passed template
#         """
#         # self.tasks = super(EmailToDo, self).add_tasks()
#         name = self.name + " (sending email)"
#         description = f"sending email task {self.name} work"
#         emailTask = EmailTask(name, self.user, self.work)
#         emailTask.set_data(description, template)
#         emailTask = emailTask.create_db_object()
#         self.tasks.append(emailTask)
#         return self.tasks
#
#
# class ContractToDo(SimpleToDo):
#     """
#     inherited SimpleToDo, and overrides the task_type and the tasks creation
#     """
#
#     def create_db_object(self):
#         """
#         calling the super/ parent create_db_object and passing the new value
#         for task_type
#         """
#         super(ContractToDo, self).create_db_object(task_type='contract-booking')
#
#     def add_tasks(self, template):
#         """
#         calling super/ parent add_tasks() to create todo task
#         and also creating the email todo task as well, using the
#         passed template
#         """
#         # self.tasks = super(ContractToDo, self).add_tasks()
#         name = self.name + " (sending contract)"
#         description = f"sending contract for booking task {self.name} work"
#         contractTask = ContractTask(name, self.user, self.work)
#         contractTask.set_data(description, template)
#         contractTask = contractTask.create_db_object()
#         self.tasks.append(contractTask)
#         return self.tasks
