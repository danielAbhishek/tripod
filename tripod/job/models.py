
from django.db import models
from django.contrib.auth import get_user_model

from company.models import Event, Package
from job.managers import EmailManager


class Job(models.Model):
    """
    Job database object
        Which holds the information of the job that are either accepted
        or not accepted by the business person
    """
    STATUSES = [
        ('req', 'Job request'),
        ('job', 'Confirmed Job')
    ]
    job_name = models.CharField(max_length=200)
    primary_client = models.ForeignKey(
        get_user_model(), on_delete=models.RESTRICT,
        related_name='primary_client')
    status = models.CharField(max_length=3, choices=STATUSES)
    workflow = models.OneToOneField(
        'Workflow', on_delete=models.SET_NULL, null=True, blank=True
    )
    event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True)
    venue = models.TextField(null=True, blank=True)
    venue_notes = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    all_day = models.BooleanField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    package = models.ForeignKey(
        Package, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    secondary_client = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='secondary_client', null=True, blank=True)
    source = models.ForeignKey(
        'Source', on_delete=models.SET_NULL, null=True, blank=True
    )
    emails = models.ForeignKey(
        'JobEmail', on_delete=models.SET_NULL, null=True, blank=True
    )
    contract = models.ForeignKey(
        'JobContract', on_delete=models.SET_NULL, null=True, blank=True
    )
    questionnaire = models.ForeignKey(
        'JobQuestionnaire', on_delete=models.SET_NULL, null=True, blank=True
    )
    completed = models.BooleanField(null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='jobCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='jobChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.job_name


class Workflow(models.Model):
    """
    Workflow database object
        which holds the info of worlflow that specifically available for job
        based on the event and other details
    """
    workflow_name = models.CharField(max_length=200)
    status = models.BooleanField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='workFlowCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='workFlowChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.workflow_name


class Work(models.Model):
    """
    Work database object
        which holds the information of the each step that is
    """
    # task_type
    EMAIL = 'email-todo'
    APPOINTMENT = 'app-todo'
    TODO = 'simple-todo'

    TASK_TYPES = [
        (EMAIL, 'E-mail'),
        (APPOINTMENT, 'Appointment'),
        (TODO, 'To-do')
    ]

    work_name = models.CharField(max_length=200)
    work_order = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    task_type = models.CharField(max_length=15, choices=TASK_TYPES)
    due_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='workCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='workChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.work_name

    def get_client(self):
        return self.job.primary_client


class Task(models.Model):
    # temple type
    EMAIL = 'em'
    CONTRACT = 'cn'
    QUESTIONNAIRE = 'qn'
    TODO = 'td'

    TEMPLATE_TYPES = [
        (EMAIL, 'email'),
        (CONTRACT, 'contract'),
        (QUESTIONNAIRE, 'questionnaire'),
        (TODO, 'to-do')
    ]

    task_name = models.CharField(max_length=200)
    work = models.ForeignKey('Work', on_delete=models.CASCADE)
    description = models.TextField()
    completed = models.BooleanField(null=True, blank=True)
    task_type = models.CharField(max_length=2, choices=TEMPLATE_TYPES)
    email_template = models.ForeignKey(
        'EmailTemplate', on_delete=models.SET_NULL, null=True, blank=True
    )
    contract_templete = models.ForeignKey(
        'ContractTemplate', on_delete=models.SET_NULL, null=True, blank=True
    )
    quest_template = models.ForeignKey(
        'QuestionnaireTemplate', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='taskCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='taskChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()
    email = EmailManager()

    def __str__(self):
        return self.task_name


class JobEmail(models.Model):
    # temple type
    SENT = 's'
    RECEIVED = 'r'

    STATUSES = [
        (SENT, 'Sent'),
        (RECEIVED, 'Received')
    ]

    email = models.TextField()
    status = models.CharField(max_length=1, choices=STATUSES)
    email_date = models.DateTimeField()

    def __str__(self):
        return self.email[:10]


class JobContract(models.Model):
    # temple type
    ACCEPTED = 'yes'
    NOT_ACCEPTED = 'no'

    STATUSES = [
        (ACCEPTED, 'Accepted'),
        (NOT_ACCEPTED, 'Not accepted')
    ]

    contract = models.TextField()
    status = models.CharField(max_length=3, choices=STATUSES)
    contract_date = models.DateTimeField()

    def __str__(self):
        return self.email[:10]


class JobQuestionnaire(models.Model):
    quest_temp = models.ForeignKey(
        'QuestionnaireTemplate', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    question_one = models.TextField()
    question_two = models.TextField()
    question_three = models.TextField()
    question_four = models.TextField()
    question_five = models.TextField()
    questionnaire_date = models.DateTimeField()


class EmailTemplate(models.Model):
    template_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    thank_you = models.TextField()
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='emailCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='emailChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.template_name


class ContractTemplate(models.Model):
    template_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    thank_you = models.TextField()
    signature = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='contractCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='contractChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.template_name


class QuestionnaireTemplate(models.Model):
    template_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    question_one = models.TextField()
    question_two = models.TextField()
    question_three = models.TextField()
    question_four = models.TextField()
    question_five = models.TextField()
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='questCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='questChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.template_name


class Source(models.Model):
    source = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.source


class TemplateField(models.Model):
    field = models.CharField(max_length=100, unique=True)
    object_field = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.field


class WorkTemplate(models.Model):
    WORK_CLASSES = [
        ('SimpleToDo', 'Simple To-Do'),
        ('EmailToDo', 'Email To-Do')
    ]
    class_object = models.CharField(max_length=30, choices=WORK_CLASSES)
    step_number = models.IntegerField()
    name = models.CharField(max_length=200)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    description = models.TextField()
    day_delta = models.IntegerField()
    completed = models.BooleanField()
    email_template = models.ForeignKey(
        'EmailTemplate', on_delete=models.SET_NULL, null=True, blank=True
    )
    contract_templete = models.ForeignKey(
        'ContractTemplate', on_delete=models.SET_NULL, null=True, blank=True
    )
    quest_template = models.ForeignKey(
        'QuestionnaireTemplate', on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return self.name
