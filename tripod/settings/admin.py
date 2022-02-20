from django.contrib import admin

from settings.models import (
    Workflow, EmailTemplate, ContractTemplate, QuestionnaireTemplate, Source,
    TemplateField, WorkTemplate
)


class WorkTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'workflow', 'step_number', 'class_object', 'name'
        )
    ordering = ('workflow', 'step_number')


admin.site.register(Workflow)
admin.site.register(EmailTemplate)
admin.site.register(ContractTemplate)
admin.site.register(QuestionnaireTemplate)
admin.site.register(Source)
admin.site.register(TemplateField)
admin.site.register(WorkTemplate, WorkTemplateAdmin)
