from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator, default_token_generator)
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template.loader import get_template
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from ...settings import (
    EMAIL_ACCOUNT_CREATION_PATH,
    EMAIL_SUBJECT_PREFIX,
    EMAIL_HOST_USER,
    EMAIL_BASE_URL,
)
import logging


logger = logging.getLogger("s3sample")


@receiver(post_save, sender=User)
def on_user_created(sender: User, instance: User, created: bool, **kwargs):
    try:
        if created:
            token_generator: PasswordResetTokenGenerator
            token_generator = default_token_generator
            tmp = get_template(
                "gui/password_handling/account_creation_email.html")
            token = token_generator.make_token(instance)
            uidb = urlsafe_base64_encode(str(instance.pk).encode("utf-8"))
            validate_email(instance.username)
            mail = tmp.render(context={
                    "user": instance,
                    "site_name": "saturn3.uniklinik-freiburg.de",
                    "base_url": EMAIL_BASE_URL,
                    "path": EMAIL_ACCOUNT_CREATION_PATH,
                    "uidb": uidb,
                    "token": token
                }
            )
            msg = EmailMultiAlternatives(
                subject=f"{EMAIL_SUBJECT_PREFIX} - Account registration",
                body=mail,
                from_email=EMAIL_HOST_USER,
                to=(instance.username,),
            )
            msg.send()

    except ValidationError:
        logger.error(
            f"Could not send email for {instance.username}. "
            "Username is not a valid email-address."
        )
