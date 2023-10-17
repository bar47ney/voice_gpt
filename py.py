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

g4f.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking
print(g4f.version) # check version
print(g4f.Provider.Ails.params)  # supported args

# Automatic selection of provider

# streamed completion
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is a cat?"}],
    stream=True,
)

for message in response:
    print(message, flush=True, end='')

# normal response
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{"role": "user", "content": "Hello"}],
)  # alterative model setting

print(response)