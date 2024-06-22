import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import os
import webbrowser
import pyfiglet

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init('sapi5')
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[0].id)

def speak(text):
    """Convert text to speech"""
    tts_engine.say(text)
    tts_engine.runAndWait()

def recognize_speech():
    """Recognize speech from the microphone"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
    except sr.RequestError:
        speak("Sorry, there was a problem with the speech recognition service.")
    return None

def open_application(command):
    """Open specified applications"""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "browser": "C:\\Users\\patil\\AppData\\Local\\Programs\\Opera GX\\launcher.exe",
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "code": "C:\\path\\to\\your\\code\\editor.exe"
    }
    for app in apps:
        if f"open {app}" in command:
            if "http" in apps[app]:
                webbrowser.open(apps[app])
            else:
                os.startfile(apps[app])
            speak(f"Opening {app.capitalize()}")
            return
    speak("Sorry, I cannot open that application.")

def input_text(command):
    """Type the specified text using pyautogui"""
    pyautogui.typewrite(command)

def wish_me():
    """Greet the user based on the time of day"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("How can I help you today?")

def execute_command(command):
    """Execute the given command"""
    if 'wikipedia' in command:
        speak('Searching Wikipedia...')
        query = command.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any results.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Sorry, the query is ambiguous. Did you mean: {e.options}?")
    elif 'open' in command:
        open_application(command)
    elif 'type' in command:
        text_to_type = command.replace("type", "").strip()
        input_text(text_to_type)
    elif 'play music' in command:
        music_dir = 'C:/Music'  # Update this path to your music directory
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
            speak("Playing music")
        else:
            speak("No music files found.")
    elif 'time' in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")
    elif 'shutdown' in command:
        speak("Shutting down the computer")
        os.system("shutdown /s /t 1")
    else:
        speak("Command not recognized.")

def start_listening():
    """Start the voice assistant"""
    wish_me()
    while True:
        command = recognize_speech()
        if command:
            execute_command(command.lower())

def start_voice_assistant():
    """Start the voice assistant in a separate thread"""
    threading.Thread(target=start_listening).start()

# GUI setup
app = tk.Tk()
app.title("Voice Assistant")

# Banner
banner_text = pyfiglet.figlet_format("VOICE ASSISTANT")
banner_label = tk.Label(app, text=banner_text, font=("Courier", 12))
banner_label.pack()

# Text widget to display recognized speech
text_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=10, font=("Courier", 12))
text_area.pack(padx=10, pady=10)

# Start button
start_button = tk.Button(app, text="Start Voice Assistant", command=start_voice_assistant, font=("Courier", 12))
start_button.pack(pady=10)

# Run the application
app.mainloop()