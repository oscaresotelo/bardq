# from bardapi import Bard

# bard = Bard(token='YwhlcoKaK4On2dndWfbCoX9MifhxeC_5mVs6d6WAHBlGs3J88otYTjI0NKeHYH4R90VSrQ.')
# audio = bard.speech('Hello, I am Bard! How can I help you today?')
import requests
from bardapi import Bard

bard = Bard(token='YwhlcoKaK4On2dndWfbCoX9MifhxeC_5mVs6d6WAHBlGs3J88otYTjI0NKeHYH4R90VSrQ.')
audio_data = bard.speech('hola, como estas soy oscar?')

# Save the audio data to an MP3 file
file_name = 'bard_audio.mp3'
with open(file_name, 'wb') as f:
    f.write(audio_data)

print(f'Audio saved to {file_name}')
