#/bin/bash
cd getWeather-Scritp-Dir
python MojiWeatherFromWeb.py
[ $? -eq 0 ] && say 'Weather copied.' && exit
python MojiWeatherFromAPI.py
[ $? -eq 0 ] && say 'Weather copied.' && exit
say 'Error occurred.' && exit 1
