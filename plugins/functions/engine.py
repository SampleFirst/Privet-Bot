import openai

async def ai(query):
    openai.api_key = "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" #Your openai api key
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Specify the model, e.g., "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.9,
        timeout=5
    )
    return response.choices[0].message['content'].strip()

async def ask_ai(client, m, message):
    try:
        question = message.text.split(" ", 1)[1]
        response = await ai(question)
        await m.edit(f"{response}")
    except Exception as e:
        error_message = f"An error occurred: {e}"
        await m.edit(error_message)
