import speech_recognition as sr  # type: ignore
from gtts import gTTS
import os
from playsound import playsound
from transformers import pipeline


# Initialize recognizer and AI model
r = sr.Recognizer()
nlp_model = pipeline("text2text-generation", model="facebook/blenderbot-400M-distill")


def speak(text):
    """Convert text to speech and play it."""
    tts = gTTS(text, lang='en')
    temp_file = "temp.mp3"  # Using a simpler file name
    tts.save(temp_file)
    playsound(temp_file)
    os.remove(temp_file)

def listen():
    """Listen for user speech and convert it to text."""
    with sr.Microphone() as source:
        print("Say Something...")
        r.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            audio = r.listen(source)  # Set timeout
            command = r.recognize_google(audio).lower()  # Convert speech to lowercase text
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return ""

def processCommand(command):
    """Process the user's command using AI."""
    response = nlp_model(command, max_length=100, num_return_sequences=1, truncation=True)
    return response[0]["generated_text"]


if __name__ == "__main__":
    speak("Good Afternoon Sir. How may I help you?")
    
    while True:
        command = listen()
        if "exit" in command or "bye" in command:  # Fixed exit condition
                speak("I'll take my leave, Sir.")
                break
        if command:
            response = processCommand(command)
            speak(response)
            
