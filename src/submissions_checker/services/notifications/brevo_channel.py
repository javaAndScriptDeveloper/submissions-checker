"""Email notification channel using Brevo API (https://brevo.com)."""

import httpx

from submissions_checker.services.notifications.base import NotificationChannel

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


class BrevoChannel(NotificationChannel):
    """Sends notifications via Brevo HTTP API."""

    def __init__(self, api_key: str, from_address: str) -> None:
        self._api_key = api_key
        self._from_address = from_address

    async def send(self, recipient: str, subject: str, body: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                BREVO_API_URL,
                headers={"api-key": self._api_key},
                json={
                    "sender": {"email": self._from_address},
                    "to": [{"email": recipient}],
                    "subject": subject,
                    "textContent": body,
                },
                timeout=15,
            )
            response.raise_for_status()
