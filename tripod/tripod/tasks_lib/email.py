
from tripod.tasks_lib.template_prepration import EmailContent, DatabaseObject


class Email:
    """
    Represent the email class, which get the content and prepare the eamil
    and sents
    --> passed as args and kwargs
    * email_template -> predefined email template
    * user -> user db object
    * company -> company db object
    * template_objects -> collection of template field objects
    -- > init by calling functions
    * email_content -> Creation of EmailContent()
    * database_objects -> Creating DatabaseObject()
    """
    def __init__(self, email_template, user, company, template_objects):
        self.email_content = EmailContent(
            email_template, subject=True, thank_you=False, signature=False
        )
        self.database_objects = DatabaseObject(user, company, template_objects)

    def get_content(self):
        """prepareing the content for email"""
        return self.email_content.prepare_content(self.database_objects)

    def send_email(self):
        """sending the email with correct content"""
        self.email_content = self.get_content()
        print(f"sending email to {self.database_objects.user.first_name}")
        print("=====================")
        print("/n")
        print(self.email_content.subject)
        print("/n")
        print(self.email_content.body)
        print("/n")
        print(self.email_content.thank_you)
