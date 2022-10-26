from django.core.mail import EmailMessage

from .models import CustomUser


def send_confirmation_email(user: CustomUser):
    """Отправка письма подтвеждающего валидность email"""

    mail_subject = 'Активируйте свой аккаунт'
    message = "Привет {0},\n вот код подтверждения {1}".format(
        user.username, user.conformation_token)
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
