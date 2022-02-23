
from django.db import models
from django.contrib.auth import get_user_model

from company.models import Event, Package
from settings.models import (
    Workflow, EmailTemplate, ContractTemplate, QuestionnaireTemplate,
    Source
)
# from job.managers import EmailManager

from tripod.tasks_lib.email import EmailClient


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
    description = models.TextField(null=True, blank=True)
    primary_client = models.ForeignKey(
        get_user_model(), on_delete=models.RESTRICT,
        related_name='primary_client')
    status = models.CharField(max_length=3, choices=STATUSES)
    workflow = models.ForeignKey(
        Workflow, on_delete=models.SET_NULL, null=True, blank=True
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
        Source, on_delete=models.SET_NULL, null=True, blank=True
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


class Work(models.Model):
    """
    Work database object
        which holds the information of the each step that is
    """
    work_name = models.CharField(max_length=200)
    work_order = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False, null=True, blank=True)
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
        EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    contract_templete = models.ForeignKey(
        ContractTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    quest_template = models.ForeignKey(
        QuestionnaireTemplate, on_delete=models.SET_NULL,
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
    # email = EmailManager()

    def __str__(self):
        return self.task_name

    def send_email(self, user):
        ec = EmailClient(self.email_template, user)
        ec.send_email()

    def send_contract_and_invoice(self, user, content):
        ec = EmailClient(self.contract_templete, user)
        ec.add_content(content)
        ec.send_email()


class JobEmail(models.Model):
    # temple type
    SENT = 's'
    RECEIVED = 'r'

    STATUSES = [
        (SENT, 'Sent'),
        (RECEIVED, 'Received')
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
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
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    contract = models.TextField()
    status = models.CharField(max_length=3, choices=STATUSES)
    contract_date = models.DateTimeField()

    def __str__(self):
        return self.email[:10]


class JobQuestionnaire(models.Model):
    quest_temp = models.ForeignKey(
        QuestionnaireTemplate, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question_one = models.TextField()
    question_two = models.TextField()
    question_three = models.TextField()
    question_four = models.TextField()
    question_five = models.TextField()
    questionnaire_date = models.DateTimeField()
