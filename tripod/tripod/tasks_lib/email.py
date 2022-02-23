
from tripod.tasks_lib.template_prepration import (
    TemplateContent, TemplateDatabaseObjects
    )

from core.models import Company
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
    def __init__(self, email_template, user):
        self.attachment = None
        self.additional_content = None
        self.template_content = TemplateContent(
            email_template, subject=True, thank_you=False, signature=False
        )
        self.company = Company.objects.filter(active=True).first()
        self.template_objects = TemplateField.objects.all()
        self.database_objects = TemplateDatabaseObjects(
            user, self.company, self.template_objects)

    def get_content(self):
        """prepareing the content for email"""
        return self.template_content.prepare_content(self.database_objects)

    def add_content(self, content, attachment=None):
        """adding additional content for email"""
        self.additional_content = content
        self.attachment = attachment

    def send_email(self):
        """sending the email with correct content"""
        self.template_content = self.get_content()
        if self.attachment:
            print("sending attachement....")
        print(f"sending email to {self.database_objects.user.first_name}")
        print("=====================")
        print("/n")
        print(self.template_content.subject)
        print("/n")
        print(self.additional_content)
        print(self.template_content.body)
        print("/n")
        print(self.template_content.thank_you)
