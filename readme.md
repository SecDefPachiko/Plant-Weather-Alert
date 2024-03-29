# Inclement Weather for Plants

This script prompts the user to enter a zip code and country code, retrieves location data for that city using the Open Weather Geocoding API. The latitude and longitude for given location is then used to retrieve weather data using OpenWeatherMap API. JSON data returned with 5 days forcast in increments of 3 hours. This data is stored in a table which is then used to query for freezing temperatures or inclement weather (ie. rain, thunderstorms, or snow). If there are any days that match the threshold the user will be notified of which day and time the forecast is expected to reach those conditions.

You can adjust the conditions and notifications according to your preferences. Weather API key can be recieved for free at "https://openweathermap.org/api". Insert key in designated variable prior to launching.

### Future implementations:
- Plant database with predetermined thresholds.
