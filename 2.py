import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary 
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    c = c.lower()
    if "google" in c:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif "facebook" in c:
        speak("Opening Facebook.")
        webbrowser.open("https://facebook.com")
    elif "youtube" in c:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
    elif "linkedin" in c:
        speak("Opening LinkedIn.")
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            speak(f"Playing {song}.")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in the music library.")
    elif "exit" in c or "quit" in c:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand that command.")


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    mic = sr.Microphone()  # Default microphone; change index if needed
    while True:
        try:
            with mic as source:
                print("Calibrating for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for the wake word...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)
            print(f"Detected word: {word}")
            if "jarvis" in word.lower():
                speak("Yes, I'm listening.")
                with mic as source:
                    print("Listening for your command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)
        except sr.WaitTimeoutError:
            print("No speech detected within the given time.")
            speak("I didn't hear anything. Can you try again?")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speak("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("There was a problem with the speech recognition service.")
        except Exception as e:
            print(f"Error: {e}")
            speak("An unexpected error occurred. Please try again.")
