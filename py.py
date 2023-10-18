# import requests
# from pyht import Client

# client = Client(  
#    user_id="Sua0mbA64INLDYxzuIx4xmSDSnE2",  
#    api_key="9f201cb006d84961806a7f56bd4b8621",  
# )

# url = "https://play.ht/api/v2/tts/stream"

# payload = {
#     "quality": "draft",
#     "output_format": "mp3",
#     "speed": 1,
#     "sample_rate": 24000,
#     "text": "Hey there, I'm calling in regards to the car you enquired yesterday.\"",
#     "voice": "larry"
# }
# headers = {
#     "accept": "audio/mpeg",
#     "content-type": "application/json",
#     "AUTHORIZATION": "Bearer 9f201cb006d84961806a7f56bd4b8621",
#     "X-USER-ID": "Sua0mbA64INLDYxzuIx4xmSDSnE2"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)

import g4f
import requests
# import pygame
# from sseclient import SSEClient



# # normal response
# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_4,
#     messages=[{"role": "user", "content": "Hello"}],
# )  # alterative model setting

# print(response)

# url = "https://play.ht/api/v2/tts/stream"

# payload = {
#     "quality": "draft",
#     "output_format": "mp3",
#     "speed": 1,
#     "sample_rate": 24000,
#     "text": f'{response}',
#     "voice": "larry"
# }
# headers = {
#     "accept": "audio/mpeg",
#     "content-type": "application/json",
#     "AUTHORIZATION": "Bearer 9f201cb006d84961806a7f56bd4b8621",
#     "X-USER-ID": "Sua0mbA64INLDYxzuIx4xmSDSnE2"
# }

# response_message = requests.post(url, json=payload, headers=headers)

# print(response_message.text)

# url = "https://api.play.ht/api/v2/tts?format=event-stream"

# payload = {
#     "text": f'{response_text}',
#     "voice": "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
#     "output_format": "wav",
#     "voice_engine": "PlayHT2.0",
#     "quality": "low"
# }
# headers = {
#     "accept": "text/event-stream",
#     "content-type": "application/json",
#     "AUTHORIZATION": "9f201cb006d84961806a7f56bd4b8621",
#     "X-USER-ID": "Sua0mbA64INLDYxzuIx4xmSDSnE2"
# }


# # print(response_text)

# response_request = requests.post(url, json=payload, headers=headers)

# print(response_request.text())

# Создаем объект SSEClient для обработки потока событий
# sse = SSEClient(response_request.content)

# # Обрабатываем события в потоке
# for event in sse:
#     if event.event == 'completed':
#         # Декодируем данные из потока
#         data = event.data
#         print(data)
# ссылка на MP3 файл
# response_data = response_request.json()
# response_url = response_data
# print(f'{response_url}')

# # загрузка файла
# response_audio = requests.get(url_answer)
# with open('answer.mp3', 'wb') as f:
#     f.write(response_audio.content)

# # инициализация pygame
# pygame.init()

# # воспроизведение файла
# pygame.mixer.music.load('answer.mp3')
# pygame.mixer.music.play()

# # ждем, пока файл не закончится
# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)

# # выключение pygame
# pygame.quit()

import pyttsx3
import PySimpleGUI as sg
from threading import Thread
import time

_ANSWER = ["", None]
_ANSWER[1] = pyttsx3.init()


g4f.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking

layout = [
    [sg.Text('Введите вопрос'), sg.InputText(key='-WORD-', do_not_clear=False)],
    [sg.Output(size=(88, 20), key='-OUTPUT-')],
    [sg.Submit("Поиск"), sg.Cancel("Закрыть")]
]

window = sg.Window('Voice of ChatGpt', layout)

class Thread1(Thread):
    def run(self):   
        # Устанавливаем параметры голоса (необязательно)
        # voices = engine.getProperty('voices')
        # engine.setProperty('voice', voices[0].id)  # Выбор конкретного голоса

        # Преобразуем текст в речь
        # text = "Привет! Это пример преобразования текста в речь."
         _ANSWER[1].say(_ANSWER[0])

        # Воспроизводим речь
         _ANSWER[1].save_to_file(f'{ _ANSWER[0]}', 'answer.mp3')
         _ANSWER[1].runAndWait()  

            
class Thread2(Thread):
        def run(self):
            view_output = ""
            for s in _ANSWER[0]:                
                time.sleep(0.01)
                window['-OUTPUT-'].update('')
                view_output += s
                print(view_output)
                # print(response_text)
                    # Создаем объект движка 

while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Закрыть'):
        _ANSWER[1].stop()
        sys.exit()
        break
    if event == 'Поиск':    
# print(g4f.version) # check version
# print(g4f.Provider.Ails.params)  # supported args

# Automatic selection of provider

# streamed completion    
        _ANSWER[0] = ""
        _ANSWER[1].stop()

        window['-OUTPUT-'].update('')
        text = values['-WORD-']

        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f'{text}'}],
            stream=True,
        )

        print("Ждите...")

        # response_text = ""

        for message in response:
            # print(message, flush=True, end='')
            _ANSWER[0] += message
            # print(response_text)
                # Создаем объект движка          
        t1 = Thread1()
        t1.start()
        t2 = Thread2()
        t2.start()

window.close()   