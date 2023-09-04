from django.core import mail
from django.utils.html import strip_tags

from django.dispatch import receiver
from django.template.loader import render_to_string

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens.

    When a token is created, an e-mail needs to be sent to the user

    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'first_name': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_url': f"http://localhost:8080/account/reset-password/?token={reset_password_token.key}"
    }
    subject = 'Property Manager Pro Password Reset Request'
    html_message = render_to_string('email/password_reset_email.html', context)
    plain_message = strip_tags(html_message)
    # TODO: create business email, update in settings.py
    from_email = 'nikolai.philipenko@gmail.com'
    to = reset_password_token.user.email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
