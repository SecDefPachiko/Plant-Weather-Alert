import requests

def get_location(api_key, zip_code, country_code):
    url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?zip={zip_code},{country_code}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def get_weather(api_key, lat, lon):
    url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def notify_user(weather_data):
    temperature = weather_data['main']['temp']
    weather_condition = weather_data['weather'][0]['main']

    if temperature < 5:
        print("Warning: It's very cold outside. Bring sensitive plants indoors.")
    elif weather_condition in ['Rain', 'Thunderstorm', 'Snow']:
        print("Warning: Inclement weather expected. Bring outdoor plants indoors.")
    else:
        print("Weather conditions are favorable for outdoor plants.")

def main():
    api_key = 'fb09dc1c4ca9f9e1b67eba7a09a53d66'
    zip_code = input("Enter the zip code: ")
    country_code = input("Enter the country code: ")
    #user input sent to get_location function to return location_data
    location_data = get_location(api_key, zip_code, country_code)
    lat = location_data['lat']
    lon = location_data['lon']
    #lat and long of location from get_location used in get_weather function to request weather data
    weather_data = get_weather(api_key, lat, lon)
    #ensures that 'main' and 'weather is present inside the json returned from get_weather function
    if 'main' in weather_data and 'weather' in weather_data:
        notify_user(weather_data)
    else:
        print("Failed to fetch weather data. Please check your city name and API key.")

if __name__ == "__main__":
    main()