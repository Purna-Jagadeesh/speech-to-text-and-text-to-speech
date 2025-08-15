import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile

# Initialize the recognizer
r = sr.Recognizer()

def speech_to_text(language_code):
    """Convert speech to text using Google Speech Recognition."""
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        r.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio, language=language_code)
            st.success(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError:
            st.error("Could not connect to Google Speech Recognition.")
            return None

def text_to_speech(text, language_code):
    """Convert text to speech using gTTS (Google Text-to-Speech)."""
    if text:
        try:
            tts = gTTS(text=text, lang=language_code)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format="audio/mp3")
        except Exception as e:
            st.error(f"TTS Error: {e}")
    else:
        st.warning("No text available for speech synthesis.")

def translate_text(text, source_lang, target_lang):
    """Translate text using Google Translator."""
    try:
        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated_text
    except Exception as e:
        st.error(f"Translation Error: {e}")
        return None

def main():
    st.title("Speech-to-Text & Translation App 🎙️🗣️")

    # Language Selection
    language_options = {
        "English": "en",
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te"
    }
    
    selected_language = st.selectbox("Choose your language:", list(language_options.keys()))
    language_code = language_options[selected_language]

    # Speech-to-Text
    if st.button("🎤 Start Speaking"):
        st.session_state.text = speech_to_text(language_code)

    if "text" in st.session_state and st.session_state.text:
        st.write("Recognized Text:", st.session_state.text)

    # Text-to-Speech
    if st.button("🔊 Listen to Recognized Text"):
        if "text" in st.session_state and st.session_state.text:
            text_to_speech(st.session_state.text, language_code)
        else:
            st.warning("Please speak first.")

    # Translation
    target_language = st.selectbox("Translate to:", list(language_options.keys()))
    target_language_code = language_options[target_language]

    if st.button("🔄 Translate"):
        if "text" in st.session_state and st.session_state.text:
            translated_text = translate_text(st.session_state.text, language_code, target_language_code)
            if translated_text:
                st.session_state.translated_text = translated_text
                st.success(f"Translated Text: {translated_text}")
        else:
            st.warning("Please speak first before translating.")

    # Speak Translated Text
    if st.button("🎧 Listen to Translated Text"):
        if "translated_text" in st.session_state and st.session_state.translated_text:
            text_to_speech(st.session_state.translated_text, target_language_code)
        else:
            st.warning("Translate something first before playing.")

if __name__ == "__main__":
    main()
