from machine import Pin, RTC
import network
import urequests
import utime
import tm1637
import time
import machine

# user data
ssid = ""  # wifi router name
pw = ""  # wifi router password
url = "http://worldtimeapi.org/api/timezone/Europe/Warsaw"  # see http://worldtimeapi.org/timezones
web_query_delay = 60000  # interval time of web JSON query
retry_delay = 5000  # interval time of retry after a failed Web query

# internal real time clock
rtc = RTC()

# wifi connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, pw)

# wait for connection
while not wifi.isconnected():
    pass

# wifi connected
print("IP:", wifi.ifconfig()[0], "\n")

# set timer
update_time = utime.ticks_ms() - web_query_delay

button3 = Pin(2, Pin.IN, Pin.PULL_UP)
button2 = Pin(0, Pin.IN, Pin.PULL_UP)
button1 = Pin(4, Pin.IN, Pin.PULL_UP)
tm = tm1637.TM1637(clk=Pin(16), dio=Pin(5))

# variables
var1 = 0
var2 = 0
Idk = 6
WOW = 17
HEH = 22
Mili = 0
Sec = 0
Min = 0
Godz = 0
Wait = 500

tm.show("Hi")
time.sleep(1)
while True:
    # if lose wifi connection, reboot ESP8266
    if not wifi.isconnected():
        machine.reset()

    # query and get web JSON every web_query_delay ms
    if utime.ticks_ms() - update_time >= web_query_delay:

        # HTTP GET data
        response = urequests.get(url)

        if response.status_code == 200:  # query success

            print("JSON response:\n", response.text)

            # parse JSON
            parsed = response.json()
            datetime_str = str(parsed["datetime"])
            year = int(datetime_str[2:4])
            month = int(datetime_str[5:7])
            day = int(datetime_str[8:10])
            hour = int(datetime_str[11:13])
            minute = int(datetime_str[14:16])
            second = int(datetime_str[17:19])
            subsecond = int(round(int(datetime_str[20:26]) / 10000))

    List = ["D " + str(day), "M " + str(month), "R " + str(year), str(hour), str(minute), str(second)]
    # auto scrolling
    if button3.value() == False & var1 < 1:
        var1 = 1
    if var1 == 1:
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
        tm.show("AUTO")
        Boobs = 2
        time.sleep(1)
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
        tm.show("ON")
        time.sleep(1)
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
    if var1 == 2:
        if var2 > len(List) - 1:
            var2 = 0
        else:
            var2 = var2 + 1
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
    if button3.value() == False and var1 > 2  :
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
        tm.show("AUTO")

        time.sleep(1)
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
        tm.show("OFF")
        time.sleep(1)
        Boobs = 0
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])

    # Buttons
    if button1.value() == False:
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
        var2 = var2 + 1
        time.sleep_ms(Wait)
        Mili = Mili + 50
    if button2.value() == False:
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
        var2 = var2 - 1
        time.sleep_ms(Wait)
        Mili = Mili + 50
    # list length
    if var2 > len(List) - 1:
        var2 = 0
    if var2 < 0:
        var2 = len(List) - 1
    # Break code
    if button2.value() == False & button1.value() == False:
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
        tm.show("Bye")
        time.sleep(1)
        tm.write([0000000000, 0000000000, 0000000000, 0000000000])
        break

    tm.show(List[var2])
    time.sleep_ms(500)
