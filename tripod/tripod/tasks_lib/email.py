
from tripod.tasks_lib.template_prepration import (
    TemplateContent, TemplateDatabaseObjects
    )

from tripod.utils import get_company
from settings.models import TemplateField


class EmailClient:
    """
    Represent the email class, which get the content and prepare the eamil
    and sents
    --> passed as args and kwargs
    * email_template -> predefined email template
    * user -> user db object
    * company -> company db object
    * template_objects -> collection of template field objects
    -- > init by calling functions
    * template_content -> Creation of TemplateContent()
    * database_objects -> Creating TemplateDatabaseObjects()
    """
    def __init__(self, task=None):
        self.task = task
        self.additional_content = None
        self.attachment = None

    def get_content(self):
        """prepareing the content for email"""
        self.email_template = self.task.email_template
        self.contract_template = self.task.contract_template
        self.company = get_company()
        self.job = self.task.get_job()
        self.user = self.job.primary_client
        self.template_objects = TemplateField.objects.all()
        self.database_objects = TemplateDatabaseObjects(
            self.company, self.task, self.template_objects)
        return self.template_content.prepare_content(self.database_objects)

    def add_content(self, content, attachment=None):
        """adding additional content for email"""
        self.additional_content = content
        self.attachment = attachment

    def send_email(self, is_task=True):
        """sending the email with correct content"""
        # creating TemplateConent based on the type
        if not is_task:
            if self.attachment:
                print("sending attachement....")
            if self.additional_content:
                print(f"sending email to {self.additional_content}")
        else:
            if self.task.task_type == 'em':
                self.template_content = TemplateContent(
                    self.task.email_template
                    )
            elif self.task.task_type == 'cn':
                self.template_content = TemplateContent(
                    self.task.contract_template
                    )
                print(self.template_content)
            elif self.task.task_type == 'ap':
                self.template_content = TemplateContent(
                    self.task.email_template
                    )
            elif self.task.task_type == 'qn':
                self.template_content = TemplateContent(
                    self.task.quest_template
                    )

            # getting content prepared
            self.template_content = self.get_content()
            if self.attachment:
                print("sending attachement....")
            if self.additional_content:
                print(self.additional_content)
            print(f"sending email to {self.database_objects.user.first_name}")
            print("=====================")
            print("/n")
            print(self.template_content.subject)
            print("/n")
            print(self.template_content.body)
            print("/n")
            print(self.template_content.thank_you)

    def book_appointment(self, appointment):
        """sending an email with an appointment recorded"""
        self.send_email()
        print('booking calender...')
        print('------> app' + appointment.description)
