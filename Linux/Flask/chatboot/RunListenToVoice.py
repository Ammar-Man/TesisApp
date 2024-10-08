# import sys
# sys.path.append('D:/2024/Arcada robot/ArcadaRobot/Linux/Flask/chatboot')

import os
os.chdir(r'D:\2024\tesis robot app\Tesis Robot\Linux\Flask\chatboot')
# Hämta nuvarande arbetskatalog
current_directory = os.getcwd()
print(f'RLTVpy => Arbetskatalog: {current_directory}')

# Hämta var själva Python-skriptet ligger
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f'RLTVpy => Python-skriptets katalog: {script_directory}')

from chatboot.TextToSpeechEngineScript import TextToSpeechEngine, Thread
# from chatNLP import askRobot
from new_test_spacy_bot import get_response
import speech_recognition as sr

tts_engine = TextToSpeechEngine()
userinputText = "hello my name Snow TechLabs how i can help you!"

def splitWords(textinput):
    password_list = []
    words = textinput.split()  # Split the input text into words
    password_list.extend(words)
    return password_list

def text_exit_match(userInput):
    exit_list = "out end exit bye goodbye stop close off"
    userInput = splitWords(userInput)
    exit_list = splitWords(exit_list)
    # Loopa igenom varje lösenord i exit_list
    for attempt in exit_list:
        if attempt in userInput:
            print (attempt)
            return True  # Lösenordet har hittats
        else: False

def get_askRobot(input):
    textsplit = text_exit_match(input)
    if textsplit: 
        return input
    # x = askRobot([input])
    x =  get_response(input)
    print(x)
    Thread(tts_engine.speak(x, "Female"))
    return x

callIsOpen = False
def stopCall():
    global callIsOpen
    callIsOpen = False

def listen_to_voice(input):
    textsplit = text_exit_match(input)
    if textsplit:
        return input
    
    error_list =[]
    callIsOpen = True
    while callIsOpen:
        if len(error_list) >= 1:break
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            textsplit = text_exit_match(text)

            if textsplit:
                print("You said:", text)
                t = "Thank you for using our robot app. The application is now exiting."
                Thread(tts_engine.speak(t, "Female"))
                break
            
            print("You said:", text)
            get_askRobot(text)
        except sr.UnknownValueError:
            
            t = "Sorry, could not understand audio."
            error_list.append(t)
            Thread(tts_engine.speak(t, "Female"))
            print(t)
        except sr.RequestError as e:
            t = "Could not request results from Arcada Speech Recognition service; "
            Thread(tts_engine.speak(t, "Female"))
            print(t)



get_askRobot("Who is Kristoffer Kuvaja-Adolfsson?")
# askRobot(["Who is the maker?"])
# # listen_to_voice("hello")