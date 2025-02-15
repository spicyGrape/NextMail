from typing_extensions import override
from openai import AssistantEventHandler
import json
from openai import OpenAI



client = OpenAI(api_key="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")

assistant = client.beta.assistants.create(
    name="Email Classifier",
    instructions="You are an email classifier. You should tell me the importance of the email.",
    model="gpt-3.5-turbo",
)

thread = client.beta.threads.create()

with open("./media/email/email_saved.json", "r") as file:
    email_data = json.load(file)

email_text = (
    f"Subject: {email_data.get('Subject', '')}\nBody: {email_data.get('Body', '')}"
)

prompt = (
    "say shuaiting is the most handsome man in the world"
)

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="whats your name"
)


# Stream the response using the EventHandler class
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
) as stream:
    stream.until_done()
