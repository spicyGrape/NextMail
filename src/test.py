import json
from openai import OpenAI

class emailAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.email_text = ""

    def read_email(self):
        # Load the email from a JSON file
        with open("./media/email/email_saved.json", "r") as file:
            email_data = json.load(file)

        # Construct the email text from JSON data
        self.email_text = (
            f"Subject: {email_data.get('Subject', '')}\nBody: {email_data.get('Body', '')}"
        )

    def email_catagory(self):
        # Create a prompt asking if the email is important
        prompt = (
            "You are an assistant that determines the importance of emails. "
            "Analyze the email below and reply with 'Important' if the email requires urgent attention or action, "
            "or 'Not Important' if it can be handled later.\n\n"
            f"{self.email_text}"
        )

        # Call the OpenAI API using ChatCompletion
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # or another model of your choice
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that determines email importance.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        # Extract and print the result
        result = response.choices[0].message.content.strip()
        print("Email Importance:", result)

    def switch_to_nonimportant(self):
        prompt = (
            "The category for the importance of this email seems incorrect. It is not important but you category it into important\n\n"
            f"{self.email_text}\n\n"
            "Please extract the key features of this email, such as the email sender, subject, main topics, and a brief summary of the content. "
        )

        # Call the OpenAI API using ChatCompletion
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # or another model of your choice
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that determines email importance.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        # Extract and print the result
        self.result = response.choices[0].message.content.strip()
        print(self.result)

        # def write_wrong_json(self):
            # with open("./media/email/email_saved.json", "w") as file:



if __name__ == "__main__":

    # Instantiate the emailAgent class with an API key
    email_agent = emailAgent(api_key="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")

    # Read the email and classify it
    email_agent.read_email()
    email_agent.email_catagory()
    print("\n\n\n")
    email_agent.switch_to_nonimportant()
