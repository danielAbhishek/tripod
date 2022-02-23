from django.db import models
from django.contrib.auth import get_user_model


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


class EmailTemplate(models.Model):
    workflow = models.ForeignKey(
        Workflow, on_delete=models.SET_NULL, null=True, blank=True)
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


class WorkType(models.Model):
    work_type = models.CharField(max_length=20)
    work_order = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.work_type


class WorkTemplate(models.Model):
    WORK_CLASSES = [
        ('SimpleToDo', 'Simple To-Do'),
        ('EmailToDo', 'Email To-Do'),
        ('ContractToDo', 'Contract To-Do')
    ]
    work_type = models.ForeignKey(
        WorkType, on_delete=models.SET_NULL, null=True, blank=True)
    class_object = models.CharField(max_length=30, choices=WORK_CLASSES)
    job_confirmation = models.BooleanField()
    step_number = models.IntegerField()
    name = models.CharField(max_length=200)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    description = models.TextField()
    auto_complete = models.BooleanField()
    day_delta = models.IntegerField(null=True, blank=True)
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
