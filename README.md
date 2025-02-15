## Environment

Dependencies:

- Python 3.13.2
- OpenAi sdk for Python

We use GPT-4o model to to classify emails, based on its importance, into 4 catologues: Important Information, Unimportant, Requires Action, Requires Reply.

We implemented the logic of classifying inside **EmailAgent.py**. We encapsulated the functions into a class. You can modify the prompt here.
