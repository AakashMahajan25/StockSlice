from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

def send_activation_email(email, token):
    subject = 'Your email needs to be verified | Djewels'
    email_from = settings.EMAIL_HOST_USER
    domain = settings.DOMAIN_NAME  # Set this value in your settings.py file
    activation_link = f'http://{domain}/account/activate/{token}'
    message = f'Click this link to activate your account: {activation_link}'
    # send_mail(subject, message, email_from, [email], fail_silently=False)
    print("email sended")
    print(activation_link)