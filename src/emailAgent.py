import json
from openai import OpenAI


class emailAgent:
    def __init__(
        self,
        api_key="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",
    ):
        self.client = OpenAI(api_key=api_key)

    # Set your OpenAI API key

    def judge_email(self):
        # Load the email from a JSON file

        with open("./media/email/email_saved.json", "r") as file:
            email_data = json.load(file)

        # Construct the email text from JSON data
        email_text = f"Subject: {email_data.get('Subject', '')}\nBody: {email_data.get('Body', '')}"

        # Create a prompt asking if the email is important
        prompt = (
            "You are an assistant that determines the importance of emails. "
            "Analyze the email below and reply with 'Important' if the email requires urgent attention or action, "
            "or 'Not Important' if it can be handled later.\n\n"
            f"{email_text}"
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
        return response.choices[0].message.content.strip()


# Extract and print the result
if __name__ == "__main__":

    agent = emailAgent()
    result = agent.judge_email()
    print("Email Importance:", result)
