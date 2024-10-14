from typing import Any

from django.conf import settings
from django.core.mail import EmailMessage as DjangoEmailMessage
from django.template.loader import render_to_string


class EmailMessage(DjangoEmailMessage):
    content_subtype = "html"


def send_email(email: str, subject: str, template: str, context: dict[str, Any]):
    html_content = render_to_string(template, context)
    email_message = EmailMessage(
        subject=subject,
        body=html_content,
        to=[email],
        from_email=f"ABC Concierge <{settings.DEFAULT_FROM_EMAIL}>",
    )
    email_message.send()
