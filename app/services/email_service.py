import logging
from email.message import EmailMessage
import aiosmtplib
import asyncio
from ..core.config import settings

logger = logging.getLogger(__name__)

class EmailError(Exception):
    """Base exception for email-related errors."""
    pass

class EmailConfigurationError(EmailError):
    """Raised when email configuration is incomplete."""
    pass

class EmailSendError(EmailError):
    """Raised when email sending fails."""
    pass

async def send_email(subject: str, body: str, to_email: str, from_email: str | None = None):
    # Validate required parameters
    if not subject or not body or not to_email:
        raise ValueError("subject, body, and to_email are required")

    from_addr = from_email or settings.FROM_EMAIL or settings.SMTP_USER or "no-reply@example.com"
    logger.debug(f"Preparing to send email to {to_email} with subject '{subject}'")

    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Check SMTP configuration
    if not (settings.SMTP_HOST and settings.SMTP_PORT and settings.SMTP_USER is not None and settings.SMTP_PASSWORD is not None):
        logger.error("SMTP configuration is incomplete. Required: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD")
        raise EmailConfigurationError("SMTP configuration is incomplete")

    try:
        logger.info(f"Sending email via SMTP to {to_email}")
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True,
        )
        logger.info(f"Email sent successfully to {to_email}")
        return True
    except aiosmtplib.SMTPException as e:
        logger.error(f"SMTP error while sending email to {to_email}: {e}")
        raise EmailSendError(f"Failed to send email via SMTP: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error while sending email to {to_email}: {e}")
        raise EmailSendError(f"Unexpected error during email sending: {e}") from e

async def notify_on_new_lead(lead):
    # Validate lead object
    if not lead or not hasattr(lead, 'id') or not hasattr(lead, 'email'):
        raise ValueError("Invalid lead object provided")

    logger.info(f"Starting email notifications for lead ID {lead.id}")

    # lead is ORM instance with attributes
    prospect_subject = "Thanks for your submission"
    prospect_body = f"Hi {lead.first_name},\n\nThank you for submitting your application. We will review and get back to you.\n\nBest regards,\nTeam"

    attorney_subject = f"New lead submitted: {lead.first_name} {lead.last_name}"
    attorney_body = (
        f"A new lead has been submitted.\n\n"
        f"Name: {lead.first_name} {lead.last_name}\n"
        f"Email: {lead.email}\n"
        f"Resume path: {lead.resume_path or 'N/A'}\n"
        f"State: {lead.state}\n"
    )

    # run both in parallel
    tasks = []
    tasks.append(send_email(prospect_subject, prospect_body, lead.email))
    if settings.ATTORNEY_EMAIL:
        tasks.append(send_email(attorney_subject, attorney_body, settings.ATTORNEY_EMAIL))
        logger.info("Added attorney notification task for %s", settings.ATTORNEY_EMAIL)
    else:
        logger.info("No attorney email configured; skipping attorney notification")
    try:
        await asyncio.gather(*tasks)
        logger.info(f"Notification emails sent successfully for lead ID {lead.id} and attrorney email {settings.ATTORNEY_EMAIL}")
    except EmailConfigurationError as e:
        logger.error(f"Email configuration error for lead ID {lead.id}: {e}")
        raise  # Re-raise configuration errors as they indicate setup issues
    except EmailSendError as e:
        logger.error(f"Failed to send notification emails for lead ID {lead.id}: {e}")
        raise EmailError(f"Email sending failed for lead {lead.id}: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error during email notifications for lead ID {lead.id}: {e}")
        raise EmailError(f"Unexpected error during email notifications: {e}") from e
