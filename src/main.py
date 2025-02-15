from EmailAccept import *
from emailAgent import *


email_fetcher = EmailFetcher("./media/email_account.json")
email_fetcher.connect()
email_data = email_fetcher.fetch_latest_email()

if email_data:
    email_fetcher.save_email_data(email_data)


agent = emailAgent()
result = agent.judge_email()
print("Subject: ", "Email Importance:", result)

email_fetcher.logout()
