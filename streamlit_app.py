'''
Source codes and pretrained parameter from https://github.com/spectraldoy/music-transformer.git

Model trained on Undertale musics by Toby Fox.
MIDI source : https://steamcommunity.com/app/391540/discussions/0/487870763294856117

'''

import os
from random import randint
import multiprocessing
import streamlit as st
import time


def generation(model_path,gen_path,temp,tempo):
    global finished
    os.system(f"python /app/music-transformer-undertale/music-transformer/generate.py {model_path} {gen_path} -v -t {temp} -tm {tempo}")
    finished = True

gen_path = "./gen_audio.mid"
wav_path = "./gen_audio.wav"
model_path = '/app/music-transformer-undertale/ThdNewSave_path.pt'

st.header("Music Generation by Transformer")
st.write('''source codes and pretrained parameter from https://github.com/spectraldoy/music-transformer.git

\nModel trained on Undertale musics by Toby Fox.
MIDI source : https://steamcommunity.com/app/391540/discussions/0/487870763294856117''')



gen_path = "./gen_audio.mid"
wav_path = "./gen_audio.wav"
model_path = '/SecondNewSave_path.pt'

tempo = st.text_input("Enter Tempo","")

choice = randint(0, 1)
temp = choice * randint(500, 800) / 1000 + (1 - choice) * randint(1000, 1200) / 1000
#!python ./music-transformer/generate.py {model_path} {gen_path} -v -t {temp} -tm {tempo}
if st.button('Generate'):
    finished = False
    while not finished:
        p = multiprocessing.Process(target=generation, name="Foo", args=(model_path,gen_path,temp,tempo))
        st.write("Generating Music...")
        p.start()
        time.sleep(10)
        p.terminate()
        p.join()
    st.write("Creating playable audio...")
    os.system(f"fluidsynth -ni Yamaha-C5-Salamander-JNv5.1.sf2 {gen_path} -F {wav_path} -r 44100 -g 1.0")
    audio_file = open('/gen_audio.wav', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)
