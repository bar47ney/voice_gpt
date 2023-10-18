import telebot
from telebot import types
import g4f
import requests
import pyttsx3
import speech_recognition as sr
import soundfile as sf

g4f.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking

bot = telebot.TeleBot('API_KEY')

engine = pyttsx3.init()

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text:        
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f'{message.text}'}],
            stream=True,
        )      
        answer = ""
        for s in response:
            # print(message, flush=True, end='')
            answer += s
        print(answer)
        # engine.say(answer)

        # Воспроизводим речь
        engine.save_to_file(f'{answer}', 'answer.wav')
        engine.runAndWait()  
        bot.send_message(message.from_user.id, f'{answer}', parse_mode='Markdown') # Отправка файла в чат
        bot.send_document(message.from_user.id, document=open("answer.wav", "rb"))
        # bot.send_audio(message.from_user.id, audio=open("answer.wav", "rb"))

    #ответ бота  
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
    #     btn1 = types.KeyboardButton('Как стать автором на Хабре?')
    #     btn2 = types.KeyboardButton('Правила сайта')
    #     btn3 = types.KeyboardButton('Советы по оформлению публикации')
    #     markup.add(btn1, btn2, btn3)
    #     bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота


    # elif message.text == 'Как стать автором на Хабре?':
    #     bot.send_message(message.from_user.id, '[ссылка](https://habr.com/ru/sandbox/start/)', parse_mode='Markdown')

    # elif message.text == 'Правила сайта':
    #     bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)', parse_mode='Markdown')

    # elif message.text == 'Советы по оформлению публикации':
    #     bot.send_message(message.from_user.id, 'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)', parse_mode='Markdown')
# from pydub import AudioSegment

# # Конвертируем OGG-файл в WAV-формат
# def convert_ogg_to_wav(ogg_file, wav_file):
#     audio = AudioSegment.from_file(ogg_file, format='ogg')
#     audio.export(wav_file, format='wav')

# # Путь к оригинальному OGG-файлу
# ogg_file_path = 'voice_message.ogg'
# # Путь для сохранения WAV-файла
# wav_file_path = 'voice_message.wav'

# # Конвертируем OGG-файл в WAV-формат
# convert_ogg_to_wav(ogg_file_path, wav_file_path)

from pydub import AudioSegment
    
global_text = ''

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # Получаем файл голосового сообщения
    voice = message.voice
    file_info = bot.get_file(voice.file_id)
    file = bot.download_file(file_info.file_path)
    # Сохраняем файл на диск
    with open('voice_answer.wav', 'wb') as f:
        f.write(file)
#     # Распознаем речь из файла
#     recognizer = sr.Recognizer() 
    
#     with sr.AudioFile('voice_message.wav') as source:
#         audio = recognizer.record(source)
#     try:
#         # Используем Google Web Speech API для распознавания речи
#         text = recognizer.recognize_google(audio, language='ru-RU')
#         bot.reply_to(message, text)
#     except sr.UnknownValueError:
#         bot.reply_to(message, "Не удалось распознать голосовое сообщение")
#     except sr.RequestError as e:
#         bot.reply_to(message, "Ошибка сервиса распознавания речи; {0}".format(e))
    # Создание экземпляра объекта Recognizer

    # Путь к исходному файлу
    input_file = 'voice_answer.wav'

    # Путь к файлу в новом формате
    output_file = 'voice_answer.flac'

    # Загрузка аудиофайла
    audio_data, sample_rate = sf.read(input_file)

    # Запись аудиофайла в новом формате (FLAC)
    sf.write(output_file, audio_data, sample_rate, format='FLAC')



    r = sr.Recognizer()
    # Открытие аудиофайла с помощью AudioFile
    with sr.AudioFile('voice_answer.flac') as source:
        # Чтение аудиоданных из файла
        audio_data = r.record(source)
        # Распознавание речи
        text = r.recognize_google(audio_data, language='ru')
        # Вывод распознанного текста
        print(text)
        global_text = text
        bot.send_message(message.from_user.id, f'{text}', parse_mode='Markdown') # Отправка файла в чат

        
        response2 = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f'{global_text}'}],
            stream=True,
        )      
        answer2 = ""
        for ss in response2:
            # print(message, flush=True, end='')
            answer2 += ss
        bot.send_message(message.from_user.id, f'{answer2}', parse_mode='Markdown') # Отправка файла в чат

bot.polling(none_stop=True, interval=0) 
#обязательная для работы бота часть