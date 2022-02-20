from django import forms

from job.models import Task

from tripod.utils import add_basic_html_tags


class TaskForm(forms.ModelForm):
    """TaskForm creation"""
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'changed_by', 'changed_at']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        self.operation = kwargs.pop('operation')
        super().__init__(*args, **kwargs)
        if self.operation == 'updating':
            self.obj = Task.objects.get(pk=self.instance.pk)
        add_basic_html_tags("Task", self.fields, True)

    def save(self, *args, **kwargs):
        if self.operation == 'creating':
            self.instance.create_by = self.user
        elif self.operation == 'updating':
            self.instance.created_by = self.obj.created_by
            self.instance.created_at = self.obj.created_at
            self.instance.id = self.obj.id
            self.instance.changed_by = self.user
        taskObj = super(TaskForm, self).save(*args, **kwargs)
        return taskObj
