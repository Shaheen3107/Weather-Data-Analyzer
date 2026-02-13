#import os
import requests
import json
from datetime import datetime

#os.chdir(r"E:\Python\2025\projects\Weather_data analyzer\weather_data.json")

CITIES = ["Bangalore", "Mumbai", "Delhi", "Kolkata", "Chennai", "Pune"]
API_KEY = "0b8aa2a7bc1e06bf9d4f249e9b1e802a"   # replace with the new working key
DATA_FILE = r"E:\Python\2025\projects\Weather_data analyzer\weather_data.json"

# Fetch weather for city
def fetch_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            print(f"Error fetching weather for {city}: {data.get('message')}")
            return None
            
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"], 
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except requests.exceptions.RequestException as e:
        print(f"Network error for {city}:{e}")
        return None
    except Exception as e:
        print(f"unexcepted error for {city}:{e}")
        return None
    
#sava data to JSON            
def save_data(weather_list):
    try:
        with open(DATA_FILE,"w") as f:
            json.dump(weather_list,f,indent = 4)
            print(f"Weather data saved succesffully to {DATA_FILE}")
    
    except Exception as e:
        print(f"error saving data : {e}")
        return None
    
#load data from JSON
def load_data():
    try:
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{DATA_FILE} not found!")
        return []
    except Exception as e:
        print(f"error loading data : {e}")
        return []
    
#analyze weather data
def analyze_weather(data):
    if not data:
        print("No data to analyze")
        return
    
    try:
        highest_temp = max(data, key = lambda x : x["temperature"])
        lowest_temp = min(data, key = lambda x : x["temperature"])
        avg_temp = sum(d["temperature"] for d in data) / len(data)
        avg_humidity = sum(d["humidity"] for d in data) / len(data)

        print("------Weather Analysis-------")
        print(f"city with highest temperature : {highest_temp['city']} {highest_temp['temperature']}")
        print(f"city with lowest temperature : {lowest_temp['city']} {lowest_temp['temperature']}")
        print(f"city with average temperature : {avg_temp:.2f}°C")
        print(f"city with average humidity : {avg_humidity:.2f}%\n")

        print("------Detailed Weather-------")
        for city_data in data:
            print(f"{city_data['city']} : {city_data['temperature']}°C, {city_data['humidity']}% humidity," 
                    f"{city_data['weather'].capitalize()}, Wind {city_data['wind_speed']} m/s")

    except Exception as e:
        print(f"error analyzing data : {e}")
        
def main():
    print("fetching weather data for cities")
    weather_list = []

    for city in CITIES:
        data = fetch_weather(city)
        if data:
            weather_list.append(data)
        else:
            print(f"No data fetched for {city}")
    print("Weather list:", weather_list)

    save_data(weather_list)
    loaded_data = load_data()
    print("Loaded data:", loaded_data)
    analyze_weather(loaded_data)

if __name__ == "__main__":
    main()
    
