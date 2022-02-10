from django.db import models
from django.contrib.auth import get_user_model

from company.models import Event, Package


class Job(models.Model):
    """
    Job database object
        Which holds the information of the job that are either accepted
        or not accepted by the business person
    """
    job_name = models.CharField(max_length=200)
    primary_client = models.ForeignKey(
        get_user_model(), on_delete=models.RESTRICT,
        related_name='primary_client')
    secondary_client = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='secondary_client', null=True, blank=True)
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
    workflow = models.ForeignKey(
        'Workflow', on_delete=models.SET_NULL, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    source = models.ForeignKey(
        'Source', on_delete=models.SET_NULL, null=True, blank=True
    )
    contract = models.ForeignKey(
        'Contract', on_delete=models.SET_NULL, null=True, blank=True
    )
    questionnaire = models.ForeignKey(
        'Questionnaire', on_delete=models.SET_NULL, null=True, blank=True
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
    # temple type
    EMAIL = 'em'
    CONTRACT = 'cn'
    QUESTIONNAIRE = 'qn'

    TEMPLATE_TYPES = [
        (EMAIL, 'email'),
        (CONTRACT, 'contract'),
        (QUESTIONNAIRE, 'questionnaire')
    ]

    work_name = models.CharField(max_length=200)
    description = models.TextField()
    task = models.ForeignKey(
        'Task', on_delete=models.SET_NULL, null=True, blank=True
    )
    template_type = models.CharField(max_length=2, choices=TEMPLATE_TYPES)
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


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    description = models.TextField()
    task_type = models.CharField(max_length=200)
    email_template = models.ForeignKey(
        'Email', on_delete=models.SET_NULL, null=True, blank=True
    )
    contract_templete = models.ForeignKey(
        'Contract', on_delete=models.SET_NULL, null=True, blank=True
    )
    quest_template = models.ForeignKey(
        'Questionnaire', on_delete=models.SET_NULL, null=True, blank=True
    )
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='taskCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='taskChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.task_name


class Workflow(models.Model):
    """
    Workflow database object
        which holds the info of worlflow that specifically available for job
        based on the event and other details
    """
    workflow_name = models.CharField(max_length=200)
    work_items = models.ManyToManyField(
        Work, through='WorkLinkFlow')
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


class WorkLinkFlow(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    work_flow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    step_numer = models.IntegerField()
    completed = models.BooleanField()
    due_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='wlwCreated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='wlwChanged', null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return (self.work + " - " + self.work_flow)


class Email(models.Model):
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


class Contract(models.Model):
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


class Questionnaire(models.Model):
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
