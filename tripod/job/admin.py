from django.contrib import admin

from job.models import (
    Job, Work, Task, JobContract, JobQuestionnaire, Appointment
)


admin.site.register(Job)
admin.site.register(Work)
admin.site.register(Task)
admin.site.register(JobContract)
admin.site.register(JobQuestionnaire)
admin.site.register(Appointment)
