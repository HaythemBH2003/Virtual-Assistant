import speech_recognition as sr
import pyttsx3
import pywhatkit
import time
import wikipedia
import datetime
import pyjokes
import webbrowser
import smtplib
import requests
from email.message import EmailMessage
listener = sr.Recognizer()
engine = pyttsx3.init()


def get_weather():
    try:
        try:
            with sr.Microphone() as source:
                alexa_talks("listening for city ...")
                voice = listener.listen(source)
                city_name = listener.recognize_google(voice)
                city_name = city_name.lower()
                print(city_name)
        except:
            pass
        #city_name = input(str("city name: "))
        api_key = "a675b10956d5856e41e31077a6763ad6"
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
        params = {"units": "metric"}
        response = requests.get(url, params=params)
        weather = response.json()
        temp = (weather["list"][0]["main"]["temp"])
        description = (weather["list"][0]["weather"][0]["description"])
        wind_speed = (weather["list"][0]["wind"]["speed"])
        forecast_date = (weather["list"][0]["dt_txt"])
        alexa_talks(f"Forecast date: {forecast_date}")
        alexa_talks(f"Temperature: {temp} degree celsius")
        alexa_talks(f"Weather description: {description}")
        alexa_talks(f"Wind speed: {wind_speed * 3.6} kilometers per hour")
        print(f"Forecast date: {forecast_date}")
        print(f"Temperature: {temp} °C")
        print(f"Sky: {description}")
        print(f"Wind speed: {wind_speed * 3.6} km/h")
    except:
        print("city not found")


def alexa_talks(text):
    engine.say(text)
    engine.runAndWait()


voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)
alexa_talks("hello")


def receiving_command():
    try:
        with sr.Microphone() as source:
            print("listening ...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "alexa" in command:
                print(command)
    except:
        pass
    return command


def execute():
    command = receiving_command()
    command = command.replace("alexa", "")
    if "play" in command:
        song = command.replace("play", "")
        alexa_talks(f"Okay! I will play music for you!")
        alexa_talks(f"playing {song}")
        pywhatkit.playonyt(song)
    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        print(current_time)
        alexa_talks(f"Current time is {current_time}")
    elif "what" and "date" in command:
        date = datetime.date.today()
        alexa_talks(f"Today is {date}")
    elif "wikipedia" in command:
        person = command.replace("wikipedia", "")
        info = wikipedia.summary(person, 1)
        print(info)
        alexa_talks(info)
    elif "single" in command:
        alexa_talks("LOL! You're the only single creature left in this world !")
    elif "joke" in command:
        alexa_talks(pyjokes.get_joke())
    elif "find location" in command:
        alexa_talks("What is the location ?")
        try:
            with sr.Microphone() as source:
                print("listening for location ...")
                voice = listener.listen(source)
                location = listener.recognize_google(voice)
                location = location.lower()
                print(location)
                url = f"https://www.google.com/maps/search/{location}/@36.8213913,10.1285888,13z/data=!3m1!4b1"
                webbrowser.get().open(url)
        except:
            pass
    elif "google search" in command:
        alexa_talks("What is the topic ?")
        try:
            with sr.Microphone() as source:
                print("listening for topic ...")
                voice = listener.listen(source)
                topic = listener.recognize_google(voice)
                topic = topic.lower()
                print(topic)
                url = f"https://www.google.com/search?q={topic}"
                webbrowser.get().open(url)
        except:
            pass
    elif "exit" in command:
        alexa_talks("Goodbye")
        exit()
    elif "open mail" in command:
        webbrowser.get().open("https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser")
    elif "send mail" in command:
        msg = EmailMessage()
        alexa_talks("Enter the subject: ")
        msg['Subject'] = input(str("Subject: "))
        alexa_talks("Enter the body: ")
        msg['Body'] = input(str("Body: "))
        alexa_talks("Enter the content: ")
        content = input(str("Context: "))
        msg.set_content(content)
        alexa_talks("Enter your address: ")
        address = input(str("Your address: "))
        msg['From'] = address
        alexa_talks("Enter your password: ")
        password = input(str("Your password: "))
        alexa_talks("Enter the receiver's address: ")
        msg['To'] = input(str("Receiver mail address: "))
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(address, password)
            smtp.send_message(msg)
    elif "weather" in command:
        get_weather()
    else:
        alexa_talks("Say it again")


while True:
    try:
        execute()
    except:
        pass
