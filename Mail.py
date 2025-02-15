import imaplib
import email
import json
import os

from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into the environment


# Configuration - update these with your server and login details
IMAP_SERVER = "imap-mail.outlook.com"
IMAP_PORT = 993
USERNAME = os.environ.get("EMAIL_USERNAME")
PASSWORD = os.environ.get("EMAIL_PASSWORD")


def get_body(msg):
    """Extracts the plain text body of the email message."""
    if msg.is_multipart():
        for part in msg.walk():
            # Look for plain text parts and ignore attachments
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="replace")
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="replace")
    return ""


def fetch_unread_emails():
    """Connects to the IMAP server, fetches unread emails, and returns a list of email data dictionaries."""
    # Connect securely to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(USERNAME, PASSWORD)

    # Select the mailbox you want to check (default is "INBOX")
    mail.select("inbox")

    # Search for unread emails (the 'UNSEEN' flag)
    status, data = mail.search(None, "UNSEEN")
    if status != "OK":
        print("Error searching inbox.")
        return []

    email_ids = data[0].split()
    emails_list = []

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        if status != "OK":
            print(f"Failed to fetch email with id {e_id}")
            continue

        # Parse the raw email content
        msg = email.message_from_bytes(msg_data[0][1])

        # Create a dictionary of the email's data
        email_data = {
            "from": msg.get("From"),
            "to": msg.get("To"),
            "subject": msg.get("Subject"),
            "date": msg.get("Date"),
            "body": get_body(msg),
        }
        emails_list.append(email_data)

    mail.logout()
    return emails_list


if __name__ == "__main__":
    emails = fetch_unread_emails()

    # Save the emails to a JSON file
    with open("emails.json", "w", encoding="utf-8") as f:
        json.dump(emails, f, ensure_ascii=False, indent=4)

    print(f"Saved {len(emails)} unread emails to emails.json")
