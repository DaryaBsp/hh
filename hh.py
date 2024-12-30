from flask import Flask, request
import requests
import logging

# Инициализация Flask приложения
app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{5515189522:AAGmRwKg3I_GHpJBN_qzSqrpHz5cAhOiuYQ}/'

# Ссылка на анкету
APPLICATION_FORM_URL = 'https://example.com/application-form'

# Приветственное сообщение
WELCOME_MESSAGE = (
    "Здравствуйте! Я бот, помогающий с трудоустройством.\n"
    "Вот что я могу для вас сделать:\n"
    "1. Ответить на вопросы о вакансии.\n"
    "2. Перевести вас на заполнение анкеты.\n"
    "Напишите свой вопрос или введите 'Анкета', чтобы перейти к заполнению."
)

# Часто задаваемые вопросы
FAQ = {
    "Какие требования к вакансии?": "Основные требования: опыт работы от 1 года, знание офисных программ, умение работать в команде.",
    "Какой график работы?": "График работы: 5/2 с 9:00 до 18:00.",
    "Какая зарплата?": "Зарплата зависит от должности и обсуждается на собеседовании.",
    "Где находится офис?": "Офис находится в центре города, рядом с метро."
}

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Функция отправки сообщений в Telegram
def send_message(chat_id, text):
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        logging.error(f"Failed to send message: {response.text}")

# Функция отправки клавиатуры
def send_keyboard(chat_id, text, options):
    url = TELEGRAM_API_URL + 'sendMessage'
    keyboard = {'keyboard': [[{'text': option}] for option in options], 'resize_keyboard': True, 'one_time_keyboard': True}
    payload = {'chat_id': chat_id, 'text': text, 'reply_markup': keyboard}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        logging.error(f"Failed to send keyboard: {response.text}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '').strip()

        logging.info(f"Received message from {chat_id}: {text}")

        if text.lower() == 'анкета':
            send_message(chat_id, f"Пожалуйста, заполните анкету по ссылке: {APPLICATION_FORM_URL}")
        elif text in FAQ:
            send_message(chat_id, FAQ[text])
        elif text.lower() == 'начать':
            send_keyboard(chat_id, "Выберите интересующий вопрос или нажмите 'Анкета' для перехода к заполнению:", list(FAQ.keys()) + ['Анкета'])
        else:
            send_message(chat_id, WELCOME_MESSAGE)

    return 'OK', 200

# Функция установки вебхука
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    webhook_url = 'https://your-server-url/webhook'
    url = TELEGRAM_API_URL + 'setWebhook'
    payload = {'url': webhook_url}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return "Webhook set successfully", 200
    else:
        return f"Failed to set webhook: {response.text}", 400

if __name__ == '__main__':
    app.run(port=5000)
