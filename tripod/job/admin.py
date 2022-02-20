from django.contrib import admin

from job.models import (
    Job, Work, Task, JobEmail, JobContract, JobQuestionnaire
)


admin.site.register(Job)
admin.site.register(Work)
admin.site.register(Task)
admin.site.register(JobEmail)
admin.site.register(JobContract)
admin.site.register(JobQuestionnaire)
