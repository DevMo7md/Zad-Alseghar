from django.core.mail import send_mail
from django.conf import settings

def send_contact_email(subject, message, user_email):
    # Email to Admin
    send_mail(
        subject=f"New Contact Message: {subject}",
        message=f"From: {user_email}\n\n{message}",
        from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
        recipient_list=[settings.DEFAULT_FROM_EMAIL or 'admin@example.com'], # Ideally admin email
        fail_silently=True,
    )

def send_reply_email(subject, reply_message, user_email):
    # Email to User
    send_mail(
        subject=f"Reply to: {subject}",
        message=reply_message,
        from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
        recipient_list=[user_email],
        fail_silently=True,
    )
