"""Email templates for quiz result notifications."""


def passed_template(github_username: str, score: int, max_score: int, lab_id: int) -> tuple[str, str]:
    """Return (subject, body) for a passing quiz result."""
    subject = f"Congratulations! You passed Lab {lab_id} Quiz"
    body = (
        f"Hi @{github_username},\n\n"
        f"Great news — you passed the Lab {lab_id} quiz!\n\n"
        f"Your score: {score}/{max_score}\n\n"
        f"Your submission is now complete. Well done!\n\n"
        f"Best regards,\nThe Teaching Team"
    )
    return subject, body


def failed_template(github_username: str, score: int, max_score: int, lab_id: int) -> tuple[str, str]:
    """Return (subject, body) for a failing quiz result."""
    subject = f"Lab {lab_id} Quiz Result — Please Resubmit"
    body = (
        f"Hi @{github_username},\n\n"
        f"Unfortunately, you did not pass the Lab {lab_id} quiz.\n\n"
        f"Your score: {score}/{max_score}\n\n"
        f"To try again, push a new commit to your PR branch — this will trigger a fresh\n"
        f"AI review and generate a new quiz for you.\n\n"
        f"Good luck!\n\n"
        f"Best regards,\nThe Teaching Team"
    )
    return subject, body
