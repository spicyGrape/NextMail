import json
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

class EventHandler(AssistantEventHandler):
    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

class EmailAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.email_text = ""
        self.assistant = self.client.beta.assistants.create(
            name="Email Classifier",

            instructions=
            '''
            You are a helperful Email classifier.

            You are going to classify an email into 4 catologues
            based on its features.

            The 4 catologues are:
            -   Important Information: If the email contains important information.
            -   Unimportant: If the email is an ad.
            -   Requires Actions: If the email requires user to do something.
            -   Requires Reply: If the email requires user to reply.

            Your response should include a word indicating which catologue it is,
            and a reason why it is.

            There should be a new line when the 'reason' part starts.

            Keep your response short and concise.
            ''',

            model="gpt-4o-mini",
        )
        self.thread = self.client.beta.threads.create()

    def read_email(self):
        # Load the email from a JSON file
        with open("../media/email/email_saved.json", "r") as file:
            email_data = json.load(file)

        # Construct the email text from JSON data
        self.email_text = (
            f"Subject: {email_data.get('Subject', '')}\nBody: {email_data.get('Body', '')}"
        )

    def email_catagory(self):
        prompt = (f"The following is the email: \n{self.email_text}\n")

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )

        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                event_handler=EventHandler(),
        ) as stream:
            stream.until_done()

if __name__ == "__main__":
    # 确保有一个有效的 OpenAI API 密钥
    API_KEY = "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"

    # 实例化 EmailAgent
    email_agent = EmailAgent(api_key=API_KEY)

    # 读取 JSON 文件中的邮件内容
    email_agent.read_email()

    # 分类邮件重要性
    email_agent.email_catagory()



