import requests
import json
import sqlite3
from datetime import datetime

def get_location(api_key, zip_code, country_code):
    url = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data


def get_weather(api_key, lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=imperial'
    response = requests.get(url)
    data = response.json()
    return data


def notify_user():
    conn = sqlite3.connect('openweather.sqlite')
    cur = conn.cursor()
    inc_condition = ['rain', 'thunderstorm', 'snow']
    
    cur.execute('''SELECT datetime FROM Weather WHERE Temp <= 32''')
    freeze_datetime = cur.fetchone()

    cur.execute('''SELECT datetime FROM Weather WHERE Condition IN ({seq})'''.format(seq=','.join(['?']*len(inc_condition))), inc_condition)
    inc_datetime = cur.fetchone()

    if len(freeze_datetime) > 0:
        for line in freeze_datetime:
            line = datetime.strptime(line, '%Y-%m-%d %H:%M:%S')
            print('Warning: There is a chance of freezing weather on', line.strftime('%a %b %d at %I%p'))

    elif len(inc_datetime) > 0:
        for line in inc_datetime:
            line = datetime.strptime(line, '%Y-%m-%d %H:%M:%S')
            print('Warning: There is a chance of inclement weather on', line.strftime('%a %b %d at %I%p'))

    else:
        print("Weather conditions are favorable for outdoor plants.")


def update_table(zip_code, country_code, lat, lon, weather_data):
    conn = sqlite3.connect('openweather.sqlite')
    cur = conn.cursor()
    location = weather_data['city']['name'] + ', ' + weather_data['city']['country']
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Weather (Zipcode INTEGER, Location TEXT, Lat REAL, Lon REAL, datetime TEXT, Temp REAL, Condition TEXT)''')
    
    for lines in weather_data['list']:
        cur.execute('''INSERT INTO Weather 
            ( Zipcode, Location, Lat, Lon, datetime, Temp, Condition )
            VALUES ( ?, ?, ?, ?, ?, ?, ? )''', 
            (zip_code, location, lat, lon, lines['dt_txt'], lines['main']['temp_min'], lines['weather'][0]['main']) )
    conn.commit()    
    conn.close()


def clearData():
	conn = sqlite3.connect('openweather.sqlite')
	conn.execute("DROP TABLE IF EXISTS Weather")
	conn.commit()
	conn.close()


def main():
    api_key = 'fb09dc1c4ca9f9e1b67eba7a09a53d66'
    clearData()
    zip_code = input("Enter the zip code: ")
    country_code = input("Enter the country code: ")

    #user input sent to get_location function to return location_data
    location_data = get_location(api_key, zip_code, country_code)

    lat = location_data['lat']
    lon = location_data['lon']

    #Latitude and longitude of location from get_location used to request weather data
    weather_data = get_weather(api_key, lat, lon)


    # ensures that 'main' and 'weather' is present inside the json returned from get_weather function
    if 'main' in weather_data['list'][0] and 'weather' in weather_data['list'][0]:
        update_table(zip_code, country_code, lat, lon, weather_data)

        notify_user()
    else:
        print("Failed to fetch weather data. Please check your city name and API key.")

if __name__ == "__main__":
    main()