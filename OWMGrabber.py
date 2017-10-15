
# coding: utf-8

# In[1]:


import pyowm
import yaml
import time
import csv
import os
from shutil import move
from more_itertools import unique_everseen


# In[2]:


csv_path = "HurricaneData/owm_houston.csv"


# In[3]:


with open('config.yml') as f:
    # use safe_load instead load
    config = yaml.safe_load(f)


# In[4]:


while True:
    owm = pyowm.OWM(config['owm_api_key'])  # You MUST provide a valid API key
    fc = owm.daily_forecast('Texas', limit=16)
    f = fc.get_forecast()
    file_exists = os.path.isfile(csv_path)
    headers = ['timestamp', 'Max.TemperatureF', 'Min.TemperatureF', 'status_short', 'status', 'wind_speed', 'wind_dir', 'cloud_coverage', 'humidity', 'pressure', 'sea_level', 'rain', 'snow']
    with open(csv_path, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writerow(headers)
        
        for w in f.get_weathers():
            rain = w.get_rain()
            snow = w.get_snow()
            temp = w.get_temperature(unit='fahrenheit')
            pres = w.get_pressure()
            wind = w.get_wind()
            to_write = [w.get_reference_time(), temp.get('max', ''), temp.get('min', ''), w.get_status(), w.get_detailed_status(), wind.get('speed', ''), wind.get('deg', ''), w.get_clouds(), w.get_humidity(), pres.get('press', ''), pres.get('sea_level', ''), rain.get('all', ''), snow.get('all', '')]
            writer.writerow(to_write)
            
    with open(csv_path,'r') as f, open(csv_path + '.new','w') as out_file:
        out_file.writelines(unique_everseen(f))
        move(csv_path + '.new', csv_path)
        
    print('written lines')
    time.sleep(60 * 60)

