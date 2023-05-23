import time
import machine
from machine import Pin, I2C
import urequests
import network
import gc
import ntptime
import ssd1306

# variables
check = 0
check0 = 0
print1 = 0
actual_time = []
error = 0
conn = 0
reboot = 0
weather_data = []

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)

# I have no fucking idea
gc.collect()

# wifi
ssid = ''
password = ''

# idk weather shit thing
city = 'Manasterzec'
country_code = 'PL'
open_weather_map_api_key = '0d2f3098efb4ab6daf11d2236b8ce887'

# Wi-Fi shitty thing
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while not station.isconnected():
    pass
print('Connection successful')
print(station.ifconfig())
open_weather_map_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country_code + '&APPID=' + open_weather_map_api_key

timezone = 2
retry_count = 3
for i in range(retry_count):
    try:
        ntptime.settime()
        conn = conn + 1
        break
    except OSError as e:
        print('connection to NTP error: ', e)
        error = error + 1
        if i == retry_count - 1:
            print('Failed to connect to the server NTP')
            time.sleep(1)
            raise

while True:
    try:
        if station.isconnected():
            gc.collect()

            # check weather
            check = check + 1
            check0 = check0 + 1
            print1 = print1 + 1
            reboot = reboot + 1

            time.sleep_ms(200)

            #reboot after 2hours
            if reboot > 18000:
                machine.reset()


            # check time

            if check0 > 5:
                UTC_OFFSET = 2 * 60 * 60  # change the '-4' according to your timezone
                actual_time = time.localtime(time.time() + UTC_OFFSET)
                # print("Local time after synchronization：%s" % str(actual_time))
                check0 = 0

            if check > 40:
                weather_data = urequests.get(open_weather_map_url)
                # print(weather_data.json())

                location = 'Loc: ' + weather_data.json().get('name') + ' - ' + weather_data.json().get('sys').get(
                    'country')

                description = 'Desc: ' + weather_data.json().get('weather')[0].get('main')

                raw_temperature = weather_data.json().get('main').get('temp') - 273.15

                # Temperature in Celsius
                temperature = 'Temp: ' + str(raw_temperature) + '*C'

                # Pressure
                pressure = 'Press: ' + str(weather_data.json().get('main').get('pressure')) + 'hPa'

                # Humidity
                humidity = 'Humidity: ' + str(weather_data.json().get('main').get('humidity')) + '%'

                # Wind
                wind = 'Wind: ' + str(weather_data.json().get('wind').get('speed')) + 'mps ' + str(
                    weather_data.json().get('wind').get('deg')) + '*'

                check = 0

            # print to console all
            if print1 > 5:

                if weather_data:
                    display.fill(0)
                    print(description)
                    print(pressure)
                    print(humidity)
                    print(location)
                    print(temperature)
                    print(wind)
                    display.text(description, 0, 0, 1)
                    display.text(pressure, 0, 10, 1)
                    display.text(humidity, 0, 20, 1)
                    #display.text(location, 0, 30, 1)
                    display.text(temperature, 0, 30, 1)
                    #display.text(wind, 0, 50, 1)
                else:
                    display.fill(0)
                    print("connecting to weather...")
                    display.text("conn to weather...", 0, 10, 1)
                if actual_time:
                    print('Current time: %02d:%02d:%02d' % (actual_time[3], actual_time[4], actual_time[5]))
                    print('Current date: %02d:%02d:%02d' % (actual_time[0], actual_time[1], actual_time[2]))
                    display.text('time: %02d:%02d:%02d' % (actual_time[3], actual_time[4], actual_time[5]), 0, 40, 1)
                    display.text('date: %02d:%02d:%02d' % (actual_time[0], actual_time[1], actual_time[2] ), 0, 50, 1)
                    print("error count: ", error)
                    print("connecting count: ", conn, "\n")
                else:
                    print("conng to time ...")
                    display.text("conn to weather...", 0, 40, 1)
                print1 = 0
            display.show()
        else:
            display.fill(0)
            display.text("Wi-Fi is not", 10, 30, 1)
            display.text("connected", 20, 40, 1)
            print("WiFi is not connected")
            display.show()
            time.sleep(1)
            machine.reset()
    except:
        print("fuck something is bad")
        machine.reset()
