import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
from tempfile import NamedTemporaryFile

st.title("🎙️ Healthcare Kiosk - Voice Assistant")

# -------------------------------
# 🗣️ Text to Speech
# -------------------------------
st.subheader("🗣️ Text to Speech")
text_input = st.text_input("Enter text to convert to speech:")

if st.button("Convert to Speech"):
    if text_input:
        tts = gTTS(text=text_input, lang='en')
        tts.save("output.mp3")  # gTTS only outputs MP3

        st.success("Text converted to speech.")
        st.audio("output.mp3", format='audio/mp3')  # Play MP3 directly without converting
    else:
        st.warning("Please enter some text.")

# -------------------------------
# 🎧 Speech to Text
# -------------------------------
st.subheader("🎧 Speech to Text")
uploaded_file = st.file_uploader("Upload a WAV audio file only", type=["wav"])

if uploaded_file is not None:
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Recognized Text:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Sorry, could not understand the audio.")
        except sr.RequestError:
            st.error("API unavailable or check your internet connection.")
