from django.contrib import admin

from job.models import (
    Job, Work, Task, Workflow, JobEmail, JobContract, JobQuestionnaire,
    EmailTemplate, ContractTemplate, QuestionnaireTemplate, Source,
    TemplateField, WorkTemplate
)


class WorkTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'workflow', 'step_number', 'class_object', 'name'
        )
    ordering = ('workflow', 'step_number')


admin.site.register(Job)
admin.site.register(Work)
admin.site.register(Task)
admin.site.register(Workflow)
admin.site.register(JobEmail)
admin.site.register(JobContract)
admin.site.register(JobQuestionnaire)
admin.site.register(EmailTemplate)
admin.site.register(ContractTemplate)
admin.site.register(QuestionnaireTemplate)
admin.site.register(Source)
admin.site.register(TemplateField)
admin.site.register(WorkTemplate, WorkTemplateAdmin)
