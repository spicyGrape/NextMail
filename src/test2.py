from typing_extensions import override
from openai import AssistantEventHandler
import json

from openai import OpenAI


client = OpenAI(api_key="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")

assistant = client.beta.assistants.create(
    name="Email Classifier",
    instructions=
    '''
    You are a helperful Email classifier.

    You are going to classify an email into 4 catologues
    based on its importance.

    The 4 catologues are:
    -   Important Information
    -   Unimportant
    -   Requires Actions
    -   Requires Reply

    Your response should include a word indicating which catologue it is,
    and a reason why it is.

    There should be a new line when the 'reason' part starts.

    Keep your response short and concise.
    ''',
    model="gpt-4o-mini"
)

thread = client.beta.threads.create()

with open("../media/email/email_saved.json", "r") as file:
    email_data = json.load(file)

email_text = (
    f"Subject: {email_data.get('Subject', '')}\nBody: {email_data.get('Body', '')}"
)

prompt = email_text

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=prompt
)

# EventHandler class to define how to handle events in the response stream
class EventHandler(AssistantEventHandler):

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)


# Stream the response using the EventHandler class
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler(),
) as stream:
    stream.until_done()
