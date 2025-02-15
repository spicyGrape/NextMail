import json
from pprint import pprint
import imaplib
import email
from email.header import decode_header
import os

# read email info
email_account_dir = "../media/email_account.json"
with open(email_account_dir, 'r') as file:
    email_account = json.load(file)

email_user = email_account['email']
email_password = email_account['password']

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Connect to Gmail's IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Log in to your email account
mail.login(email_user, email_password)

# Select the inbox folder
mail.select("inbox")

# Search for all emails
status, messages = mail.search(None, "ALL")

# Convert the result to a list of email IDs
mail_ids = messages[0].split()

# Get the latest email
latest_email_id = mail_ids[-1]

# Fetch the email's data
status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

# Dictionary to store email details
email_data = {}

# Parse the email
for response_part in msg_data:
    if isinstance(response_part, tuple):
        # Parse the email content
        msg = email.message_from_bytes(response_part[1])

        # Get the email sender
        from_ = msg.get("From")

        # Decode the subject of the email
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        # Store the email details in the dictionary
        email_data["From"] = from_
        email_data["Subject"] = subject

        # If the email is multipart, check each part
        if msg.is_multipart():
            for part in msg.walk():
                # Get the content type of the email part
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # If the email part is plain text, get the body
                if "attachment" not in content_disposition and content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    email_data["Body"] = body
        else:
            # If the email is not multipart, just get the body
            body = msg.get_payload(decode=True).decode()
            email_data["Body"] = body

# Save the email details to a JSON file
email_save_dir = "../media/email/"

# check dir
if not os.path.exists(email_save_dir):
    os.makedirs(email_save_dir)
    print(f"{email_save_dir} -> created")



with open(f"{email_save_dir}/email_saved.json", "w") as json_file:
    json.dump(email_data, json_file, indent=4)

# Log out and close the connection
mail.logout()

print("Email data saved to email_data.json")

