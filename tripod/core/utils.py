from tripod.tasks_lib.email import EmailClient


def send_code(user):
    """sending email with the template"""
    email_body = f"""
    sending confirmation code
    {user.password_change_code}
    """
    ec = EmailClient()
    ec.add_content(email_body)
    ec.send_email(template_type=None)
