from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailService:
    @staticmethod
    def send_confirm_email(user ,subject,template,to,context):
        subject = subject
        message = render_to_string(template,context)
        plain_message = strip_tags(message)
        from_email = 'cyrusmwendwa370@gmail.com'
        to = to
        
        send_mail(subject,plain_message,from_email,[to],html_message=message)
                
         