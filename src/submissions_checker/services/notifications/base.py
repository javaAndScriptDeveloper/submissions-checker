"""Base notification channel abstraction."""

from abc import ABC, abstractmethod


class NotificationChannel(ABC):
    """Abstract base for notification delivery channels.

    Implement this class to add a new channel (Slack, SMS, etc.).
    Register the new channel in dispatcher.py's build_dispatcher().
    """

    @abstractmethod
    async def send(self, recipient: str, subject: str, body: str) -> None:
        """Send a notification to recipient.

        Args:
            recipient: Channel-specific address (email, phone number, user ID, etc.)
            subject: Short summary line
            body: Full message text
        """
