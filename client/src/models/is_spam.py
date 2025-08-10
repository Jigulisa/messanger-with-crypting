from openai import OpenAI

client = OpenAI()
def make_request(message):
    response = client.responses.create(
        model="gpt-5",
        input=f"I have a message. if it is spam (meaningless), answer 1, otherwise, answer 0. Message: '{message}'"
    )
    return response