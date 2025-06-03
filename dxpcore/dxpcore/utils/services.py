

def send_mail(receipient: list, subject: str, message: str) -> None:
    """
    Send an email
    """
    print("Email Sent To... ", receipient)
    print("Subject: ", subject)
    print("Message: ", message)