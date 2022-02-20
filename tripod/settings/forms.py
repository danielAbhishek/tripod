from django import forms

from tripod.utils import add_basic_html_tags
from settings.models import (
    Workflow, EmailTemplate, Source, TemplateField, WorkTemplate
)


class WorkflowForm(forms.ModelForm):
    """Workflow object creation"""
    class Meta:
        model = Workflow
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'changed_by', 'changed_at']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        self.operation = kwargs.pop('operation')
        super().__init__(*args, **kwargs)
        if self.operation == 'updating':
            self.obj = Workflow.objects.get(pk=self.instance.pk)
        add_basic_html_tags("Workflow", self.fields, True)

    def save(self, *args, **kwargs):
        if self.operation == 'creating':
            self.instance.create_by = self.user
        elif self.operation == 'updating':
            self.instance.created_by = self.obj.created_by
            self.instance.created_at = self.obj.created_at
            self.instance.id = self.obj.id
            self.instance.changed_by = self.user
        workFlowObj = super(WorkflowForm, self).save(*args, **kwargs)
        return workFlowObj


class EmailTemplateForm(forms.ModelForm):
    """Workflow object creation"""
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'changed_by', 'changed_at']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        self.operation = kwargs.pop('operation')
        super().__init__(*args, **kwargs)
        if self.operation == 'updating':
            self.obj = EmailTemplate.objects.get(pk=self.instance.pk)
        add_basic_html_tags("EmailTemplate", self.fields, False)

    def save(self, *args, **kwargs):
        if self.operation == 'creating':
            self.instance.create_by = self.user
        elif self.operation == 'updating':
            self.instance.created_by = self.obj.created_by
            self.instance.created_at = self.obj.created_at
            self.instance.id = self.obj.id
            self.instance.changed_by = self.user
        emailTempObj = super(EmailTemplateForm, self).save(*args, **kwargs)
        return emailTempObj


class SourceForm(forms.ModelForm):
    """Workflow object creation"""
    class Meta:
        model = Source
        fields = '__all__'


class TemplateFieldForm(forms.ModelForm):
    """Workflow object creation"""
    class Meta:
        model = TemplateField
        fields = '__all__'


class WorkTemplateForm(forms.ModelForm):
    """Workflow object creation"""
    class Meta:
        model = WorkTemplate
        fields = '__all__'
