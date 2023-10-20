import torch
# import tacotron2
# import waveglow
# from text import text_to_sequence
# from text import text_to_sequence
from torchtext.data.utils import get_tokenizer


# Загрузка предобученных моделей Tacotron 2 и WaveGlow
# # model = Tacotron2()
# tacotron2_checkpoint = torch.load('tacotron2_statedict.pt', map_location=torch.device('cpu'))
# tacotron2.load_state_dict(tacotron2_checkpoint['state_dict'])
# tacotron2.eval()

# tacotron2 = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tacotron2', map_location="cpu")
# tacotron2 = tacotron2.to('cpu')
# tacotron2.eval()

tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2', pretrained=True, force_reload=True)

checkpoint = torch.hub.load_state_dict_from_url('https://api.ngc.nvidia.com/v2/models/nvidia/tacotron2pyt_fp32/versions/1/files/nvidia_tacotron2pyt_fp32_20190306.pth', map_location="cpu")

# Unwrap the DistributedDataParallel module
# module.layer -> layer
state_dict = {key.replace("module.", ""): value for key, value in checkpoint["state_dict"].items()}


# Apply the state dict to the model
tacotron2.load_state_dict(state_dict)
tacotron2 = tacotron2.to('cpu')
tacotron2.eval()

# waveglow = WaveGlow()
# waveglow_checkpoint = torch.load('waveglow_256channels_universal_v5.pt')
# waveglow.load_state_dict(waveglow_checkpoint['state_dict'])
# waveglow.eval()

waveglow = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_waveglow', pretrained=True, force_reload=True)
waveglow = waveglow.remove_weightnorm(waveglow)
waveglow = waveglow.to('cpu')
waveglow.eval()


text = "Hello world, I missed you so much."

utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tts_utils')
sequences, lengths = utils.prepare_input_sequence([text], cpu_run=True)

with torch.no_grad():
    mel, _, _ = tacotron2.infer(sequences, lengths)
    audio = waveglow.infer(mel)
audio_numpy = audio[0].data.cpu().numpy()
rate = 22050

from scipy.io.wavfile import write
write("audio.wav", rate, audio_numpy)

from IPython.display import Audio
Audio(audio_numpy, rate=rate)
# # Функция для генерации речи на основе текста
# def generate_speech(text):
#     sequence = torch.LongTensor(text_to_sequence(text))
#     sequence = sequence.unsqueeze(0)
#     mel_outputs, mel_outputs_postnet, _, _ = tacotron2.inference(sequence)
#     with torch.no_grad():
#         audio = waveglow.infer(mel_outputs_postnet)
#     audio = audio.squeeze().cpu().numpy()
#     return audio

# # Генерация речи на основе текста
# text = "Привет, это голосовой клон!"
# audio = generate_speech(text)

# # Сохранение аудио в файл
# torch.save(audio, 'cloned_voice.wav')