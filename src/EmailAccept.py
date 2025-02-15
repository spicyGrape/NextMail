import json
import imaplib
import email
from email.header import decode_header
import os


class EmailFetcher:
    def __init__(self, email_account_path, email_save_dir="./media/email"):
        """
        Initialize the EmailFetcher instance by loading email credentials and
        setting up server details and save directory.

        :param email_account_path: Path to the JSON file containing email credentials.
        :param email_save_dir: Directory to save the fetched email details.
        """
        # Load email credentials from the provided JSON file
        with open(email_account_path, "r") as file:
            email_account = json.load(file)

        self.email_user = email_account["email"]
        self.email_password = email_account["password"]
        self.email_save_dir = email_save_dir

        # IMAP server configuration for Gmail
        self.IMAP_SERVER = "imap.gmail.com"
        self.IMAP_PORT = 993
        self.mail = None

    def connect(self):
        """
        Connect to the IMAP server and log in using the provided credentials.
        """
        self.mail = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        self.mail.login(self.email_user, self.email_password)
        self.mail.select("inbox")

    def fetch_latest_email(self):
        """
        Fetch the latest email from the inbox, parse its content, and return
        a dictionary with the email details (sender, subject, and body).

        :return: A dictionary containing the latest email's details.
        """
        if self.mail is None:
            raise Exception("Not connected to the IMAP server. Call connect() first.")

        # Search for all emails in the inbox
        status, messages = self.mail.search(None, "ALL")
        mail_ids = messages[0].split()

        if not mail_ids:
            print("No emails found in the inbox.")
            return {}

        # Fetch the latest email using its ID
        latest_email_id = mail_ids[-1]
        status, msg_data = self.mail.fetch(latest_email_id, "(RFC822)")

        email_data = {}

        # Parse the email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Retrieve sender
                from_ = msg.get("From")
                email_data["From"] = from_

                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                email_data["Subject"] = subject

                # Retrieve the email body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        # Look for plain text parts that are not attachments
                        if (
                            "attachment" not in content_disposition
                            and content_type == "text/plain"
                        ):
                            body = part.get_payload(decode=True)
                            email_data["Body"] = body.decode() if body else ""
                            break  # Stop after finding the first plain text part
                else:
                    body = msg.get_payload(decode=True)
                    email_data["Body"] = body.decode() if body else ""
        return email_data

    def save_email_data(self, email_data):
        """
        Save the email details into a JSON file in the specified directory.

        :param email_data: Dictionary containing email details.
        """
        if not os.path.exists(self.email_save_dir):
            os.makedirs(self.email_save_dir)
            print(f"{self.email_save_dir} -> created")

        save_path = os.path.join(self.email_save_dir, "email_saved.json")
        with open(save_path, "w") as json_file:
            json.dump(email_data, json_file, indent=4)
        print(f"Email data saved to {save_path}")

    def logout(self):
        """
        Log out from the IMAP server.
        """
        if self.mail:
            self.mail.logout()


if __name__ == "__main__":
    # Example usage:
    email_fetcher = EmailFetcher("./media/email_account.json")
    email_fetcher.connect()
    email_data = email_fetcher.fetch_latest_email()

    if email_data:
        email_fetcher.save_email_data(email_data)

    email_fetcher.logout()
