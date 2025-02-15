import json
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

#EventHandler for OpenAI
class EventHandler(AssistantEventHandler):
    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

#Encapsulated as an Email Agent class
class EmailAgent:
    #Get key and Generate Client
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.email_text = ""
        self.assistant = self.client.beta.assistants.create(
            name="Email Classifier",

            #Write the initial prompt
            instructions=
            '''
            You are a helperful Email classifier.

            You will be given an email or a feedback.

            If that is an email, then you are going to classify an email into 4 catologues
            based on its features.

            The 4 catologues are:
            -   Important Information: If the email contains important information.
            -   Unimportant: If the email is an ad.
            -   Requires Actions: If the email requires user to do something.
            -   Requires Reply: If the email requires user to reply.

            Your response should include a word indicating which catologue it is,
            and a reason why it is.

            There should be a new line when the 'reason' part starts.

            If that is a feedback,

            the feedback will say whether you did the right job.

            If not, you are going to re-classify the email.

            Keep your response short and concise.
            ''',

            #Specify the model
            model="gpt-4o-mini",
        )

        #Create a thread
        self.thread = self.client.beta.threads.create()


    #Method to load the Json file
    def read_email(self):
        # Load the email from a JSON file
        with open("../media/email/email_saved.json", "r") as file:
            email_data = json.load(file)

        # Construct the email text from JSON data
        self.email_text = (
            f"Subject: {email_data.get('Subject', '')}\nBody: {email_data.get('Body', '')}"
        )

    #Method to category the email
    def email_catagory(self):
        #Write prompt
        prompt = (f"The following is the email: \n{self.email_text}\n")

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )

    #Method for feedback that GPT is wrong
    def switch_to_nonImportant(self):
        prompt = (f"Your classifying for the this email is wrong.")

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )

    #Print out the response from gpt
    def print(self):

        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                event_handler=EventHandler(),
        ) as stream:
            stream.until_done()


if __name__ == "__main__":
    #Your Key
    API_KEY = "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"

    email_agent = EmailAgent(api_key=API_KEY)

    #Usage:
    #Read the email
    #Catogry the email or Give Feedback
    #Print the message
    email_agent.read_email()
    email_agent.switch_to_nonImportant()
    email_agent.print()



