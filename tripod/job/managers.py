# from django.db import models
#
# from job.utils import get_company
# from tripod.tasks_lib.email import EmailClient
#
#
# class EmailManager(models.Manager):
#     """
#     Manager class to hanlde all email related automatoin under the
#     Task model object
#     """
#     def send_email(self, id, template_objects):
#         """
#         by passing task id and collection of
#         template -> TemplateField.objects.all() email will be sent correctly
#         """
#         task = super().get_queryset().get(id=id)
#         et = task.email_template
#         user = task.work.get_client()
#         # company = get_company()
#         email = EmailClient(et, user)
#         email.send_email()
