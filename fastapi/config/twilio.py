from django.conf import settings
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_verification_code(email: str):
    verification = client.verify.services(
        settings.TWILIO_VERIFY_SERVICE
    ).verifications.create(to=email, channel="email")
    assert verification.status == "pending"


def check_verification_code(email: str, code: str):
    verification = client.verify.services(
        settings.TWILIO_VERIFY_SERVICE
    ).verification_checks.create(to=email, code=code)
    return verification.status == "approved"
