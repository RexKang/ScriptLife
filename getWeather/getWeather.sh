#/bin/bash
cd getWeather-Scritp-Dir
python MojiWeatherFromWeb.py
[ $? -eq 0 ] && say 'Weather copied.' && exit
python MojiWeatherFromAPI.py
[ $? -eq 0 ] && say 'Weather copied.' && exit
say 'Error occurred.'
echo "☀️🌤⛅️☁️🌦🌧⛈🌨，25 ~ 32℃，🌪北风？级，💧？%，🌱🍃🍂75"
exit 1
