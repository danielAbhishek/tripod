from django import forms

from job.models import Job
from job.workflow_factory.workflow import WorkFlowBase
from tripod.utils import add_basic_html_tags


class JobCreateForm(forms.ModelForm):
    """Workflow object creation"""
    class Meta:
        model = Job
        fields = [
            'job_name', 'primary_client', 'status', 'workflow', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)
        add_basic_html_tags("Job", self.fields, True)

    def save(self, *args, **kwargs):
        self.instance.create_by = self.user
        jobObj = super(JobCreateForm, self).save(*args, **kwargs)
        if jobObj.status == 'job':
            wfb = WorkFlowBase(self.user, jobObj)
            wfb.create_work_and_tasks()
        return jobObj
