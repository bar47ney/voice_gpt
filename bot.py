import telebot
from telebot import types
import g4f
import requests
import pyttsx3
import speech_recognition as sr
import soundfile as sf
from pydub import AudioSegment
from elevenlabs import set_api_key, voices, generate, save
from elevenlabs.api import Voice, Models

API_KEY = ''
set_api_key(API_KEY)
voice_id_serg = ''
voice_id_helena = ''
voice_id_kirk = ''

# voices = voices()

voice = Voice.from_id(voice_id_kirk)
voice.settings.stability = 0.3

def generate_my_voice(text):
    audio = generate(
        text=text,                # Defautls to env variable ELEVEN_API_KEY, or None if not set but quota will be limited
        voice=voice,                 # Either a voice name, voice_id, or Voice object (use voice object to control stability and similarity_boost)
        model="eleven_multilingual_v2",                                  # [1-4] the higher the more optimized for streaming latency (only works with stream=True)
    )

    save(
        audio=audio,               # Audio bytes (returned by generate)
        filename='sergey_answer.wav'               # Filename to save audio to (e.g. "sergey_answer.wav")
    )

g4f.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking

bot = telebot.TeleBot('')

# engine = pyttsx3.init()

def get_answer(message):       
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f'{message}'}],
        stream=True,
    )         
    response_answer = ""
    for s in response:
        response_answer += s
    return response_answer    

# def load_message(text='Подождите немного...'):
    # bot.send_message(message.from_user.id, f'{text}', parse_mode='Markdown') # Отправка файла в чат


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text:  
        bot.send_message(message.from_user.id, 'Подождите немного...', parse_mode='Markdown') # Отправка файла в чат
        # engine.say(answer)
        answer = get_answer(message.text)
        bot.send_message(message.from_user.id, f'{answer}', parse_mode='Markdown') # Отправка файла в чат
        # Воспроизводим речь
        # engine.save_to_file(f'{answer}', 'answer.wav')
        # engine.runAndWait()  
        generate_my_voice(answer)
        bot.send_document(message.from_user.id, document=open("sergey_answer.wav", "rb"))
        # bot.send_audio(message.from_user.id, audio=open("answer.wav", "rb"))
    
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    bot.send_message(message.from_user.id, 'Подождите немного...', parse_mode='Markdown') # Отправка файла в чат
    # Получаем файл голосового сообщения
    voice = message.voice
    file_info = bot.get_file(voice.file_id)
    file = bot.download_file(file_info.file_path)
    with open('voice_answer.wav', 'wb') as f:
        f.write(file)
    input_file = 'voice_answer.wav'
    output_file = 'voice_answer.flac'
    audio_data, sample_rate = sf.read(input_file)
    sf.write(output_file, audio_data, sample_rate, format='FLAC')
    r = sr.Recognizer()
    with sr.AudioFile('voice_answer.flac') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='ru')

        bot.send_message(message.from_user.id, f'Ищу "{text}..."', parse_mode='Markdown') # Отправка файла в чат

        answer_from_voice = get_answer(text)
        bot.send_message(message.from_user.id, f'{answer_from_voice}', parse_mode='Markdown') # Отправка файла в чат
        
        
        bot.send_message(message.from_user.id, 'Проговорю вам ответ...', parse_mode='Markdown') # Отправка файла в чат
        # engine.save_to_file(f'{answer_from_voice}', 'answer_from_voice.wav')
        # engine.runAndWait()
        generate_my_voice(answer_from_voice)
        bot.send_document(message.from_user.id, document=open("sergey_answer.wav", "rb"))

# Обработчик аудиосообщений
@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    # Получение информации о файле
    file_info_audio = bot.get_file(message.audio.file_id)
    file_audio = bot.download_file(file_info_audio.file_path)

    # Сохранение файла на диск
    with open('audio_file.wav', 'wb') as audio_file:
        audio_file.write(file_audio)
    
    input_file_audio = 'audio_file.wav'
    output_file_audio = 'audio_file.flac'
    audio_data_audio, sample_rate_audio = sf.read(input_file_audio)
    sf.write(output_file_audio, audio_data_audio, sample_rate_audio, format='FLAC')    

    # Преобразование аудио в текст
    r = sr.Recognizer()
    with sr.AudioFile('audio_file.flac') as source:
        audio_data = r.record(source)
        audio_file_text = r.recognize_google(audio_data, language='ru')  # Здесь можно указать нужный язык

    # Отправка текстового сообщения
    
    print(audio_file_text)
    bot.send_message(message.from_user.id, f'{audio_file_text}', parse_mode='Markdown') # Отправка файла в чат

bot.polling(none_stop=True, interval=0) 
#обязательная для работы бота часть