"""
Email notification helpers for the Lost & Found system.
All outgoing emails are sent from here — one function per event.
Each function is wrapped in try/except so a failed send never crashes the site.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def _send(subject, template, context, to_email):
    """Internal helper — renders template, strips to plain text, sends."""
    try:
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        # Log the error but never let email failure break the request
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Email send failed to {to_email} | subject: {subject} | error: {e}")


# ---------------------------------------------------------------------------
# Account emails
# ---------------------------------------------------------------------------

def send_welcome_email(user):
    """Sent immediately after a new account is created and approved."""
    _send(
        subject="Welcome to Lost & Found!",
        template="emails/welcome.html",
        context={"user": user},
        to_email=user.email,
    )


def send_teacher_pending_email(user):
    """Sent to a teacher after registration to inform them their account is pending admin approval."""
    _send(
        subject="Teacher Account Pending Approval — Lost & Found",
        template="emails/teacher_pending.html",
        context={"user": user},
        to_email=user.email,
    )


def send_teacher_approved_email(user):
    """Sent to a teacher when an admin approves their account."""
    _send(
        subject="Your Teacher Account Has Been Approved — Lost & Found",
        template="emails/teacher_approved.html",
        context={"user": user},
        to_email=user.email,
    )


def send_teacher_rejected_email(user):
    """Sent to a teacher when an admin rejects their account."""
    _send(
        subject="Teacher Account Registration Update — Lost & Found",
        template="emails/teacher_rejected.html",
        context={"user": user},
        to_email=user.email,
    )


# ---------------------------------------------------------------------------
# Item emails
# ---------------------------------------------------------------------------

def send_item_reported_email(user, item):
    """Sent to the reporter when they successfully submit a found item."""
    _send(
        subject=f"Item Report Received: {item.name}",
        template="emails/item_reported.html",
        context={"user": user, "item": item},
        to_email=user.email,
    )


def send_item_approved_email(user, item):
    """Sent to the reporter when an admin approves their item report."""
    _send(
        subject=f"Your Item Has Been Approved: {item.name}",
        template="emails/item_approved.html",
        context={"user": user, "item": item},
        to_email=user.email,
    )


def send_item_rejected_email(user, item, notes=""):
    """Sent to the reporter when an admin rejects their item report."""
    _send(
        subject=f"Item Report Update: {item.name}",
        template="emails/item_rejected.html",
        context={"user": user, "item": item, "notes": notes},
        to_email=user.email,
    )


def send_item_discarded_email(user, item):
    """
    Sent to the claimant (if any) when an item they were pursuing is discarded.
    Also sent to the original reporter.
    """
    _send(
        subject=f"Item No Longer Available: {item.name}",
        template="emails/item_discarded.html",
        context={"user": user, "item": item},
        to_email=user.email,
    )


# ---------------------------------------------------------------------------
# Claim emails
# ---------------------------------------------------------------------------

def send_claim_submitted_email(user, claim):
    """Sent to the claimant when they submit a claim."""
    _send(
        subject=f"Claim Submitted: {claim.item.name}",
        template="emails/claim_submitted.html",
        context={"user": user, "claim": claim},
        to_email=user.email,
    )


def send_claim_approved_email(user, claim):
    """Sent to the claimant when an admin approves their claim."""
    _send(
        subject=f"Claim Approved: {claim.item.name}",
        template="emails/claim_approved.html",
        context={"user": user, "claim": claim},
        to_email=user.email,
    )


def send_claim_rejected_email(user, claim):
    """Sent to the claimant when an admin rejects their claim."""
    _send(
        subject=f"Claim Update: {claim.item.name}",
        template="emails/claim_rejected.html",
        context={"user": user, "claim": claim},
        to_email=user.email,
    )


def send_claim_completed_email(user, claim):
    """Sent to the claimant when an item is marked as returned to them."""
    _send(
        subject=f"Item Returned: {claim.item.name}",
        template="emails/claim_completed.html",
        context={"user": user, "claim": claim},
        to_email=user.email,
    )