import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import datetime
import requests

listener = sr.Recognizer()
machine = pyttsx3.init()
genai.configure(api_key="AIzaSyDq9RHVWiUzU2ta-_Iz_lRbGp-qW0ylSF0")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config)

convo = model.start_chat(history=[])

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            speech = listener.listen(source)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
        return instruction
    except sr.UnknownValueError:
        talk("Sorry, I didn't catch that. Please repeat.")
        return None
    except sr.RequestError:
        talk("Sorry, there was an issue with accessing the speech recognition service.")
        return None

def get_weather(city):
    api_key = "9d2301f00d073d76754bcfc8e5085927"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] == 200:
        weather_info = f"The weather in {city} is {data['weather'][0]['description']} with a temperature of {data['main']['temp']}°C."
        return weather_info
    else:
        return "Sorry, I couldn't fetch the weather information."

def play_gemini():
    try:
        instruction = input_instruction()
        print(instruction)
        if instruction:
            if 'time' in instruction:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time is ' + current_time)
            elif 'weather' in instruction:
                city = instruction.split(" ")[-1]  # Assuming the city name is at the end of the instruction
                weather_info = get_weather(city)
                talk(weather_info)
            else:
                convo.send_message(instruction)
                info = convo.last.text
                print(f"Gemini: {info}")
                talk(info)
    except TypeError as e:
        print("Error:", e)

if __name__ == '__main__':
    print("Initializing Gemini...")
    play_gemini()


