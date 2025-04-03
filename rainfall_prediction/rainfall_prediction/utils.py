# import requests

# def get_weather_data(city="Ernakulam", api_key="8ad1235e6068564cccc9e11d0b0b6ebd"):
#     try:
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
#         response = requests.get(url)
#         data = response.json()

#         if response.status_code == 200:
#             weather_data = {
#                 'temperature': data['main']['temp'],
#                 'humidity': data['main']['humidity'],
#                 'pressure': data['main']['pressure'],
#                 'wind_speed': data['wind']['speed'],
#                 'description': data['weather'][0]['description'],
#                 'city': data['name'],
#             }
#             return weather_data
#         else:
#             return {'error': data.get('message', 'Error fetching data')}
#     except Exception as e:
#         return {'error': str(e)}


# ====================================================================================

# import os
# from dotenv import load_dotenv
# import requests

# # Load .env variables
# load_dotenv()

# # Get API key
# OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# def get_weather_data(city="Ernakulam"):
#     try:
#         if not OPENWEATHER_API_KEY:
#             raise Exception("API key is missing. Please set it in the .env file.")
        
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
#         response = requests.get(url)
#         data = response.json()

#         if response.status_code == 200:
#             weather_data = {
#                 'temperature': data['main']['temp'],
#                 'humidity': data['main']['humidity'],
#                 'pressure': data['main']['pressure'],
#                 'wind_speed': data['wind']['speed'],
#                 'description': data['weather'][0]['description'],
#                 'city': data['name'],
#             }
#             return weather_data
#         else:
#             return {'error': data.get('message', 'Error fetching data')}
#     except Exception as e:
#         return {'error': str(e)}

# ============================================================================================




import os
from dotenv import load_dotenv
import requests

# Load .env variables
load_dotenv()

# Get API key
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_weather_data(city="Ernakulam"):
    try:
        if not OPENWEATHER_API_KEY:
            raise Exception("API key is missing or invalid. Please set a valid API key in the .env file.")
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Check for API error using status code
        if response.status_code == 200:
            weather_data = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'city': data['name'],
            }
            return weather_data
        else:
            return {'error': f"API Error: {data.get('message', 'Error fetching data')}"}
    
    except requests.exceptions.RequestException as e:
        return {'error': f"Request failed: {str(e)}"}
    except Exception as e:
        return {'error': str(e)}
