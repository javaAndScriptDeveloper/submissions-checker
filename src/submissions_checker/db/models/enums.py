"""Database enums for type safety."""

import enum


class OutboxEventType(str, enum.Enum):
    """
    Outbox message event types.

    Defines the types of events that can be processed via the transactional outbox.
    Using an enum ensures type safety and prevents typos in event type strings.
    """

    # Pull repository code and run tests
    PULL = "PULL"

    # Perform AI code review
    REVIEW = "REVIEW"

    # Send notifications and post results
    NOTIFY = "NOTIFY"

    # Generate quiz questions from AI review
    GENERATE_QUIZ = "GENERATE_QUIZ"

    # Send quiz result notification to student via email
    NOTIFY_QUIZ_RESULT = "NOTIFY_QUIZ_RESULT"

    def __str__(self) -> str:
        """Return the string value of the enum."""
        return self.value


class OutboxMessageState(str, enum.Enum):
    """
    Outbox message processing states.

    Defines the lifecycle states of an outbox message:
    - PENDING: Message created, awaiting processing
    - FINISHED: Message processed successfully
    - ERROR: Message processing failed, will be retried
    """

    PENDING = "pending"
    FINISHED = "finished"
    ERROR = "error"

    def __str__(self) -> str:
        """Return the string value of the enum."""
        return self.value


class SubmissionStatus(str, enum.Enum):
    """
    Submission processing status.

    Defines the lifecycle states of a student submission:
    - PENDING: Submission created, awaiting clone
    - CLONING: Repository being cloned
    - REVIEWING: AI review in progress
    - COMPLETED: All processing complete
    - FAILED: Processing failed
    """

    PENDING = "pending"
    CLONING = "cloning"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self) -> str:
        """Return the string value of the enum."""
        return self.value
