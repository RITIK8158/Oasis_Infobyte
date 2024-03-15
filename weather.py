import customtkinter
import requests
from tkinter import *

font1 = ('Arial', 60, 'bold')

def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  # Use metric units for Celsius
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        weather_info = {
            "Temperature": f"{data['main']['temp']} °C",
            "Humidity": f"{data['main']['humidity']}%",
            "Weather": data['weather'][0]['description']
        }
        return weather_info
    else:
        return {"error": data["message"]}

def show_weather():
    location = city_entry.get()
    weather_data = get_weather(api_key, location)

    if "error" in weather_data:
        result_label.config(text=f"Error: {weather_data['error']}")
    else:
        result_label.config(text="Current Weather:")
        for key, value in weather_data.items():
            result_label.config(text=result_label.cget("text") + f"\n{key}: {value}")

root = customtkinter.CTk()
root.title("Weather App")

api_key = "db61f369ba267578357dc2c861e52a86"

city_label = Label(root,text="Enter City:", font = font1)
city_label.pack()

city_entry = Entry(root, font=font1)
city_entry.pack()

search_btn = customtkinter.CTkButton(root, text="Check Weather", command=show_weather,text_color='#fff',fg_color='#06911f', hover_color='#06911f', bg_color='#000', font=font1, corner_radius=5)
search_btn.pack()

result_label = Label(root, text="", justify=LEFT, font=font1)
result_label.pack()

root.mainloop()

