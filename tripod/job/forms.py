from django import forms

from job.models import Job
from job.workflow_factory.workflow import WorkFlowBase

from finance.utils import register_invoice_data_for_job

from tripod.utils import add_basic_html_tags


class JobReqCreateForm(forms.ModelForm):
    """Workflow object creation"""
    class Meta:
        model = Job
        fields = [
            'job_name', 'primary_client', 'workflow', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)
        add_basic_html_tags("Job", self.fields, True)

    def save(self, *args, **kwargs):
        self.instance.create_by = self.user
        self.instance.status = 'req'
        jobObj = super(JobReqCreateForm, self).save(*args, **kwargs)
        return jobObj


class JobUpdateConfirmForm(forms.ModelForm):
    """Workflow object creation for confirmed job"""
    class Meta:
        model = Job
        fields = '__all__'
        exclude = [
            'status', 'completed', 'created_by', 'created_at',
            'changed_by', 'changed_at']

    def __init__(self, *args, **kwargs):
        self.operation = kwargs.pop('operation')
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)
        self.obj = Job.objects.get(pk=self.instance.pk)

    def save(self, *args, **kwargs):
        self.instance.created_by = self.obj.created_by
        self.instance.created_at = self.obj.created_at
        self.instance.id = self.obj.id
        self.instance.changed_by = self.user
        if not self.instance.workflow:
            raise Exception('Workflow is needed to confirm the job')
        if self.operation == 'confirming Job':
            self.instance.status = 'job'
            jobObj = super(JobUpdateConfirmForm, self).save(*args, **kwargs)
            wfb = WorkFlowBase(self.user, jobObj)
            wfb.create_work_and_tasks()
        else:
            jobObj = super(JobUpdateConfirmForm, self).save(*args, **kwargs)
        register_invoice_data_for_job(jobObj)
        return jobObj
