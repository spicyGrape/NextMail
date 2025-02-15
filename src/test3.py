import json
from openai import OpenAI

from src.test2 import prompt


class EmailAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.email_text = ""
        self.assistant = self.client.beta.assistants.create(
            name="Email Classifier",
            instructions="You are a email classifier, you should tell me the importance of the email",
            model="gpt-3.5-turbo",
        )
        self.thread = self.client.beta.threads.create()

    def read_email(self):
        # Load the email from a JSON file
        with open("./media/email/email_saved.json", "r") as file:
            email_data = json.load(file)

        # Construct the email text from JSON data
        self.email_text = (
            f"Subject: {email_data.get('Subject', '')}\nBody: {email_data.get('Body', '')}"
        )

    def email_catagory(self):
        prompt = (
            "You are an assistant that determines the importance of emails. "
            "Analyze the email below and reply with 'Important' if the email requires urgent attention or action, "
            "or 'Not Important' if it can be handled later.\n\n"
            f"{self.email_text}"
        )

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )

        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
        ) as stream:
            stream.until_done()

