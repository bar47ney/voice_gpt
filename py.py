import requests
from pyht import Client

client = Client(  
   user_id="Sua0mbA64INLDYxzuIx4xmSDSnE2",  
   api_key="9f201cb006d84961806a7f56bd4b8621",  
)

url = "https://play.ht/api/v2/tts/stream"

payload = {
    "quality": "draft",
    "output_format": "mp3",
    "speed": 1,
    "sample_rate": 24000,
    "text": "Hey there, I'm calling in regards to the car you enquired yesterday.\"",
    "voice": "larry"
}
headers = {
    "accept": "audio/mpeg",
    "content-type": "application/json",
    "AUTHORIZATION": "Bearer 9f201cb006d84961806a7f56bd4b8621",
    "X-USER-ID": "Sua0mbA64INLDYxzuIx4xmSDSnE2"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)