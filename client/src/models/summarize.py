from openai import OpenAI

client = OpenAI()


def make_request(messages: list):
    response = client.responses.create(
        model="gpt-5",
        input=f"I have some messages. I want you to summarize the discussion. Messages: '{messages}'",
    )
    return response
