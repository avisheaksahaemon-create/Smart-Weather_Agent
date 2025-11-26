#Full Project build by Avisheak Saha Emon

import requests
import pyttsx3
import time

# Initialize TTS engine
engine = pyttsx3.init()

# Choose female voice
voices = engine.getProperty('voices')
female_voice = None
for voice in voices:
    if "female" in voice.name.lower():
        female_voice = voice
        break

if female_voice:
    engine.setProperty('voice', female_voice.id)
else:
    engine.setProperty('voice', voices[1].id)  # fallback

# Make speech softer and more human-like
engine.setProperty('rate', 145)    # slower
engine.setProperty('volume', 0.85) # softer

def speak(text):
    # Add small pauses for more natural speech
    text = text.replace('.', '. ')  # pause after sentences
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)  # small pause after speaking

def get_location():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        return data.get("city")
    except:
        return None

def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return f"The weather in {city_name} is {weather_desc}, with a temperature of {temp}°C, humidity of {humidity}%, and wind speed of {wind_speed} meters per second."
    else:
        return "Sorry, I couldn't find the weather for that city. Please check the city name."

def weather_agent():
    API_KEY = "Your API key"  # Replace with your OpenWeatherMap API key
    print("🌤️ Hello! I'm your Smart Weather Agent.")
    speak("Hello! I'm your Smart Weather Agent.")

    city = get_location()
    if city:
        response = get_weather(city, API_KEY)
        print(f"Weather Agent: {response}")
        speak(response)
    else:
        speak("I could not detect your location automatically.")
        print("Could not detect location. Please type your city manually.")

    print("\nYou can also type any city name to check weather, or type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            goodbye_text = "Goodbye! Stay safe and have a nice day!"
            print(f"Weather Agent: {goodbye_text}")
            speak(goodbye_text)
            break
        response = get_weather(user_input, API_KEY)
        print(f"Weather Agent: {response}")
        speak(response)

# Start the agent

weather_agent()
