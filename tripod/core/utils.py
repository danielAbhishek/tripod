from tripod.tasks_lib.email import EmailClient


def send_code(user):
    """sending email with the template"""
    # creating email
    subject = "Password reset code"
    body = f"Please use the this reset code \n {user.password_change_code} \n\n *DON'T SHARE WITH ANYONE*"
    ec = EmailClient()
    ec.new_content(body, subject, user.email)
    ec.send_email(is_task=False)
