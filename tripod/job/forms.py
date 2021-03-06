from django import forms

from job.models import Job, Appointment
from core.models import CustomUser
from core.models import CustomUser
from job.workflow_factory.workflow import WorkFlowBase

from finance.utils import register_invoice_data_for_job

from tripod.utils import add_basic_html_tags


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class JobCreateForm(forms.ModelForm):
    """job creating for testing purpose"""

    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['created_at', 'changed_at']
        widgets = {
            'start_date': DateInput(),
            'start_time': TimeInput(),
            'end_date': DateInput(),
            'end_time': TimeInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)
        add_basic_html_tags("Please add job - ", self.fields, True)
        self.fields['photographer'].queryset = CustomUser.objects.filter(
            is_staff=True).filter(is_photographer=True)

    def save(self, *args, **kwargs):
        self.instance.create_by = self.user
        self.instance.status = 'req'
        jobObj = super(JobCreateForm, self).save(*args, **kwargs)
        return jobObj


class JobReqCreateForm(forms.ModelForm):
    """Workflow object creation"""

    class Meta:
        model = Job
        fields = [
            'job_name', 'primary_client', 'workflow', 'description', 'source',
            'photographer'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)
        add_basic_html_tags("Please add job - ", self.fields, True)
        self.fields['photographer'].queryset = CustomUser.objects.filter(
            is_staff=True).filter(is_photographer=True)

    def save(self, *args, **kwargs):
        self.instance.created_by = self.user
        self.instance.status = 'req'
        jobObj = super(JobReqCreateForm, self).save(*args, **kwargs)
        return jobObj


class JobUpdateConfirmForm(forms.ModelForm):
    """Workflow object creation for confirmed job"""

    class Meta:
        model = Job
        fields = '__all__'
        exclude = [
            'status', 'completed', 'created_by', 'created_at', 'changed_by',
            'changed_at', 'task_status'
        ]
        widgets = {
            'start_date': DateInput(),
            'start_time': TimeInput(),
            'end_date': DateInput(),
            'end_time': TimeInput(),
        }

    def __init__(self, *args, **kwargs):
        self.operation = kwargs.pop('operation')
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)
        self.obj = Job.objects.get(pk=self.instance.pk)
        self.fields['photographer'].queryset = CustomUser.objects.filter(
            is_staff=True).filter(is_photographer=True)

    def save(self, *args, **kwargs):
        self.instance.created_by = self.obj.created_by
        self.instance.created_at = self.obj.created_at
        self.instance.id = self.obj.id
        self.instance.changed_by = self.user
        # workflow is needed

        if self.operation == 'confirming Job':
            if not self.instance.workflow:
                raise ValueError('Workflow is needed to confirm the job')
            else:
                self.instance.status = 'job'
                jobObj = super(JobUpdateConfirmForm,
                               self).save(*args, **kwargs)
                wfb = WorkFlowBase(self.user, jobObj)
                wfb.create_work_and_tasks()
        else:
            jobObj = super(JobUpdateConfirmForm, self).save(*args, **kwargs)
        if jobObj.package:
            register_invoice_data_for_job(jobObj, package=True)
        else:
            register_invoice_data_for_job(jobObj, package=False)
        return jobObj


class AppointmentForm(forms.ModelForm):
    """Appointment object creation for task"""

    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'start_date': DateInput(),
            'start_time': TimeInput(),
            'end_date': DateInput(),
            'end_time': TimeInput(),
        }
