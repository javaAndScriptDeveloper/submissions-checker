"""Email notification channel using SMTP."""

from email.message import EmailMessage

import aiosmtplib

from submissions_checker.services.notifications.base import NotificationChannel


class EmailChannel(NotificationChannel):
    """Sends notifications via SMTP email."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str | None,
        password: str | None,
        from_address: str,
        use_tls: bool,
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._from_address = from_address
        self._use_tls = use_tls

    async def send(self, recipient: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["From"] = self._from_address
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)

        await aiosmtplib.send(
            msg,
            hostname=self._host,
            port=self._port,
            username=self._username,
            password=self._password,
            start_tls=self._use_tls,
        )
