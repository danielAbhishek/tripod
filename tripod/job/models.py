from django.db import models
from django.contrib.auth import get_user_model

from company.models import Event, Package
from settings.models import (Workflow, EmailTemplate, ContractTemplate,
                             QuestionnaireTemplate, Source)
# from job.managers import EmailManager

from tripod.tasks_lib.email import EmailClient

from finance.models import Invoice
from finance.utils import prepare_invoice_sharing


class Job(models.Model):
    """
    Job database object
        Which holds the information of the job that are either accepted
        or not accepted by the business person
    """
    STATUSES = [('req', 'Job request'), ('job', 'Confirmed Job'),
                ('dec', 'Declined Job')]
    TASKCHOICES = [('jbr', 'Job request done'), ('cnb', 'Contract book done'),
                   ('jbc', 'Job confirmed'), ('prs', 'Pre-shoot done'),
                   ('mns', 'Main-shoot done'), ('pos', 'Post-shoot done'),
                   ('jbd', 'Job Done')]
    job_name = models.CharField(max_length=200)
    job_request = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    primary_client = models.ForeignKey(get_user_model(),
                                       on_delete=models.RESTRICT,
                                       related_name='primary_client')
    status = models.CharField(max_length=3, choices=STATUSES)
    task_status = models.CharField(max_length=3,
                                   choices=TASKCHOICES,
                                   null=True,
                                   blank=True)
    workflow = models.ForeignKey(Workflow,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    event = models.ForeignKey(Event,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    venue = models.TextField(null=True, blank=True)
    venue_notes = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    all_day = models.BooleanField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    package = models.ForeignKey(Package,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    note = models.TextField(null=True, blank=True)
    secondary_client = models.ForeignKey(get_user_model(),
                                         on_delete=models.SET_NULL,
                                         related_name='secondary_client',
                                         null=True,
                                         blank=True)
    source = models.ForeignKey(Source,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    completed = models.BooleanField(null=True, blank=True)
    invoice = models.OneToOneField(Invoice,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='jobCreated',
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='jobChanged',
                                   null=True,
                                   blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.job_name

    def get_user_appointment_tasks(self):
        """getting appointment tasks"""
        app_tasks = []
        works = self.work_set.all()
        for work in works:
            tasks = work.get_user_appointment_tasks()
            for task in tasks:
                if task:
                    app_tasks.append(task)
        return app_tasks

    def get_user_contract_tasks(self):
        """getting contract tasks"""
        contr_tasks = []
        works = self.work_set.all()
        for work in works:
            tasks = work.get_user_contract_tasks()
            for task in tasks:
                if task:
                    contr_tasks.append(task)
        return contr_tasks

    def get_user_quest_tasks(self):
        """getting questionnaire tasks"""
        quest_tasks = []
        works = self.work_set.all()
        for work in works:
            tasks = work.get_user_quest_tasks()
            for task in tasks:
                if task:
                    quest_tasks.append(task)
        return quest_tasks

    def get_job_completion_in_numbers(self):
        if self.task_status == 'jbr':
            return 1
        elif self.task_status == 'cnb':
            return 2
        elif self.task_status == 'jbc':
            return 3
        elif self.task_status == 'prs':
            return 4
        elif self.task_status == 'mns':
            return 5
        elif self.task_status == 'pos':
            return 6
        elif self.task_status == 'jbd':
            return 7
        else:
            return None

    def invoiced_client(self):
        """Checking if the invoice is fully paid"""
        if self.invoice.to_be_paid() > 0:
            return False
        return True


class Appointment(models.Model):
    """
    All the appointments are tracked and managed
    """
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.description[:10]


class Work(models.Model):
    """
    Work database object
        which holds the information of the each step that is
    """
    work_name = models.CharField(max_length=200)
    work_order = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False, null=True, blank=True)
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='workCreated',
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='workChanged',
                                   null=True,
                                   blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.work_name

    def get_client(self):
        return self.job.primary_client

    def get_user_appointment_tasks(self):
        """returning list of appointment tasks"""
        tasks = self.task_set.filter(task_type='ap')
        return tasks

    def get_user_contract_tasks(self):
        """returning contract task"""
        tasks = self.task_set.filter(task_type='cn')
        return tasks

    def get_user_quest_tasks(self):
        """returning questionnaire task"""
        tasks = self.task_set.filter(task_type='qn')
        return tasks

    def work_completed_percentage(self):
        """
        returning the completed work percentage
        """
        tasks = self.task_set.all()
        return self.tasks_completed_percentage(tasks)

    def work_completion_update(self):
        """
        if all tasks completed update work
        """
        if int(self.work_completed_percentage()) == 100:
            self.completed = True
            self.save()
            if self.work_name == "Job request":
                self.job.task_status = 'jbr'
            elif self.work_name == 'Contract booking':
                self.job.task_status = 'cnb'
            elif self.work_name == "Job confirmation":
                self.job.task_status = 'jbc'
            elif self.work_name == "Pre shoot":
                self.job.task_status = 'prs'
            elif self.work_name == "Main shoot":
                self.job.task_status = 'mns'
            elif self.work_name == "Post shoot":
                self.job.task_status = 'pos'
            elif self.work_name == "Job Done":
                self.job.task_status = 'jbd'
            self.job.save()

    @staticmethod
    def tasks_completed_percentage(tasks):
        """
        return tasks completed percenage by
        taking list of tasks
        """
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.completed])
        try:
            return int((completed_tasks / total_tasks) * 100)
        except ZeroDivisionError:
            return 0


class Task(models.Model):
    # temple type
    EMAIL = 'em'
    CONTRACT = 'cn'
    QUESTIONNAIRE = 'qn'
    TODO = 'td'
    APPOINTMENT = 'ap'

    TEMPLATE_TYPES = [(EMAIL, 'email'), (CONTRACT, 'contract'),
                      (QUESTIONNAIRE, 'questionnaire'), (TODO, 'to-do'),
                      (APPOINTMENT, 'appointment')]

    SEND_USER = [('no', 'Pending'), ('su', 'Sent To User'),
                 ('uc', 'User Completed')]

    task_name = models.CharField(max_length=200)
    task_order = models.IntegerField()
    work = models.ForeignKey('Work', on_delete=models.CASCADE)
    description = models.TextField()
    completed = models.BooleanField(null=True, blank=True)
    task_type = models.CharField(max_length=2, choices=TEMPLATE_TYPES)
    check_invoice = models.BooleanField(null=True, blank=True)
    appointment = models.ForeignKey('Appointment',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)
    job_contract = models.ForeignKey('JobContract',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True)
    job_quest = models.ForeignKey('JobQuestionnaire',
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True)
    email_template = models.ForeignKey(EmailTemplate,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True)
    contract_template = models.ForeignKey(ContractTemplate,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True)
    quest_template = models.ForeignKey(QuestionnaireTemplate,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True)
    user_task = models.BooleanField(null=True, blank=True)
    user_completed = models.CharField(max_length=2,
                                      choices=SEND_USER,
                                      null=True,
                                      blank=True)
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='taskCreated',
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='taskChanged',
                                   null=True,
                                   blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    # email = EmailManager()

    def __str__(self):
        return self.task_name

    def get_job(self):
        """Getting job that's for task"""
        job = self.work.job
        return job

    def job_package_added(self):
        """Checking wether the job package is available"""
        if self.get_job().package:
            return True
        else:
            False

    def send_email(self):
        """sending email with the template"""
        ec = EmailClient(self)
        ec.send_email()

    def checking_current_work_process(self):
        """gettin current working process stage"""
        return self.work.job.get_job_completion_in_numbers()

    def register_appointment(self, method):
        """registering appointment"""
        job = self.get_job()
        job_date = job.start_date if job.start_date else None
        job_end_day = job.end_date if job.end_date else None
        job_start_time = job.start_time if job.start_time else None
        job_end_time = job.end_time if job.end_time else None
        if method == 'creating':
            app = Appointment.objects.create(start_date=job_date,
                                             end_date=job_end_day,
                                             start_time=job_start_time,
                                             end_time=job_end_time,
                                             description=f"""
                    Making an appointment
                    {job_date} - from {job_start_time} to {job_end_time}
                    {self.description}
                """)
        else:
            app = self.appointment
            app.start_date = job_date
            app.end_date = job_end_day
            app.start_time = job_start_time
            app.end_time = job_end_time
            app.description = f"""
                Making an appointment
                {job_date} - from {job_start_time} to {job_end_time}
                {self.description}
            """
            app.save()
        return app

    def update_user_completed(self, reset=False):
        """
        updating user completed
        """
        if self.user_task:
            if reset:
                return 'no'
            elif self.user_completed == 'no':
                return 'su'
            elif self.user_completed == 'su':
                return 'uc'
            else:
                return 'uc'
        else:
            return None

    def update_task_completed(self, reset=False):
        """
        updating task completion
        """
        if self.user_task:
            if self.user_completed == 'uc':
                return True
            else:
                return False
        else:
            return True

    def send_contract_and_invoice(self):
        """sending contract and invoice"""
        if self.job_package_added():
            content = prepare_invoice_sharing(self.get_job())
            # preparing email to send
            ec = EmailClient(self)
            ec.add_content(content)
            ec.send_email()
            # adding contract job
            try:
                jobContract = JobContract.objects.get(job=self.get_job())
                jobContract.contract = ec.template_content.body
                jobContract.status = 'no'
                jobContract.save()
            except JobContract.DoesNotExist:
                jobContract = JobContract.objects.create(
                    job=self.get_job(),
                    contract=ec.template_content.body,
                    status='no',
                )
            self.job_contract = jobContract
            self.user_completed = 'su'
            self.save()
        else:
            raise Exception(
                'Please select the package before generating invoice')

    def send_questionnaire(self):
        """sending questionnaire to fill"""
        ec = EmailClient(self)
        ec.send_email()
        # adding questionnaire job
        try:
            jobQuest = JobQuestionnaire.objects.get(job=self.get_job())
            jobQuest.quest_temp = self.quest_template
            jobQuest.save()
        except JobQuestionnaire.DoesNotExist:
            jobQuest = JobQuestionnaire.objects.create(
                quest_temp=self.quest_template, job=self.get_job())
        self.job_quest = jobQuest
        self.user_completed = 'su'
        self.save()

    def send_appointment_email(self):
        """sending email with the appointment"""
        if not self.appointment:
            raise Excpetion('Please add job event detail correctly')
        ec = EmailClient(self)
        ec.book_appointment(self.appointment)
        self.completed = True
        self.save()

    def process_task(self, user):
        """processing task based on the task type"""
        j_status = self.checking_current_work_process()
        """
        Checking if the preceeding tasks were completed before
        continuing with the next steps
        """
        # if it is the first step then making sure first step only can be completed
        if j_status is None:
            if self.work.work_order > 1:
                raise Exception(
                    'Cannot process before completing previous tasks')
        # if it is next steps, then making sure that completed task and
        # currently trying to complete current task are next to each other
        else:
            if self.work.work_order - j_status > 1:
                raise Exception(
                    'Cannot process before completing previous tasks')

        # checking invoice should be completed
        if self.check_invoice:
            if not self.get_job().invoiced_client():
                raise Exception('Invoice is not paid or updated completely')

        if self.completed == True:
            raise Exception("Task is already completed")

        # checking user responds needed task
        if not self.user_task:
            if self.task_type == 'em':
                self.send_email()
            self.completed = True
            self.save()
        elif self.user_task:
            # contract task and user did not completed yet
            if self.task_type == 'cn' and self.user_completed == 'no':
                self.send_contract_and_invoice()
            # questionnaire task and user did not completed yet
            elif self.task_type == 'qn' and self.user_completed == 'no':
                self.send_questionnaire()
            # appointment task and user did not completed yet
            elif self.task_type == 'ap' and self.user_completed == 'no':
                self.user_completed = 'su'
                self.save()
            # appointment task and user completed
            elif self.task_type == 'ap' and self.user_completed == 'uc':
                self.send_appointment_email()
            # all the other tasks user completed
            elif self.user_completed == 'uc':
                self.completed = True
                self.save()
            else:
                raise Exception('this cannot be...')
        else:
            raise Exception('cannot be processed')

        self.work.work_completion_update()


class JobContract(models.Model):
    # temple type
    ACCEPTED = 'yes'
    NOT_ACCEPTED = 'no'

    STATUSES = [(ACCEPTED, 'Accepted'), (NOT_ACCEPTED, 'Not accepted')]
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    contract = models.TextField()
    status = models.CharField(max_length=3, choices=STATUSES)
    contract_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.job_name + " - " + self.contract[:10]


class JobQuestionnaire(models.Model):
    quest_temp = models.ForeignKey(QuestionnaireTemplate,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    answer_one = models.TextField(null=True, blank=True)
    answer_two = models.TextField(null=True, blank=True)
    answer_three = models.TextField(null=True, blank=True)
    answer_four = models.TextField(null=True, blank=True)
    answer_five = models.TextField(null=True, blank=True)
    answer_date = models.DateTimeField(null=True, blank=True)
