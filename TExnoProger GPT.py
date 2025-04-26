import telebot
import requests
from openai import OpenAI
from datetime import datetime
bot = telebot.TeleBot('8094647476:AAG-LJ8xPwZ48k4g-L26xyQwAIjflZAUEq4')
client = OpenAI(
    base_url="https://api.langdock.com/openai/eu/v1",
    api_key="sk-7R61ZWf5JwybYYMaMfGD3VRntOUOQsWhmifD-bzisozo3NZu-DrlgImLIV5v-D07PLXf6mnDULte2zM1QoKYcA"
)
NEWS_API_KEY = 'ee58ae79b7174efc8cb97cec9853eb06'
def get_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        if articles:
            news_summary = ""
            for article in articles[:5]:  # Отримуємо перші 5 статей
                title = article['title']
                description = article['description']
                url = article['url']
                news_summary += f"**{title}**\n{description}\n{url}\n\n"
            return news_summary
        else:
            return "Немає новин за вашим запитом."
    else:
        return "Помилка при отриманні новин."
@bot.message_handler(commands=['start'])
def start_handler(message):
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id,f'Привіт, {first_name}! Я TechnoProer IA! Напиши мені будь-яке питання, і я дам на нього відповідь!')
@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    user_input = message.text.lower()
    if 'який сьогодні день' in user_input:
        now = datetime.now()
        formatted_date = now.strftime("%d.%m.%Y")
        formatted_time = now.strftime("%H:%M")
        reply = f"Сьогодні {formatted_date}, час: {formatted_time}."

    elif 'коли ти зроблений' in user_input:
        username = "𝕮𝖔𝖉𝖊𝕮𝖆𝖙"
        reply = f"Я був створений создателем {username} та запущений 26 квітня 2025 року о 10:00. Моя мета — допомагати вам!"

    elif 'де тьолки' in user_input:
        reply = "Дівчата можуть бути в різних місцях, наприклад, у парку, в кафе, на заходах або в навчальних закладах. Просто потрібно бути ввічливим і шукати відповідне місце для знайомства."
    elif 'новини' in user_input:
        query = user_input.replace('новини', '').strip()  # Очищаємо запит від слова 'новини'
        if query:
            reply = get_news(query)
        else:
            reply = "Будь ласка, уточніть, про які новини ви хочете дізнатися."
    else:
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ти — універсальний асистент.\n\n"
                            "- Якщо користувач задає питання про людей, події або факти, відповідай коротко, чітко і ввічливо.\n"
                            "- Якщо користувач пише математичну задачу або вираз, тоді:\n"
                            "    * Вводь змінні через літери.\n"
                            "    * Оформи всі обчислення у звичайному текстовому вигляді (без LaTeX і без спеціальних символів).\n"
                            "    * Пояснюй рішення крок за кроком простими реченнями.\n"
                            "    * В кінці завжди окремо пиши відповідь у форматі: Відповідь: ...\n"
                            "- Формулюй відповідь так, ніби пояснюєш її живій людині.\n"
                            "- Не перепитуй, одразу давай відповідь."
                        )
                    },
                    {"role": "user", "content": user_input}
                ]
            )
            reply = completion.choices[0].message.content
        except Exception as e:
            reply = "Виникла помилка при зверненні до GPT 😕"
    bot.send_message(message.chat.id, reply)
print("Бот запущено!")
bot.polling()

