import openai

openai.api_key = "Введи сюди свій api_key"
question = "Що таке Python?"  # Введи своє запитання

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=question,
    max_tokens=1024,
    temperature=0.7,
    n=1,
    format="text",
)

print(response.choices[0].text[2:])  # Виведення відповіді у консоль
