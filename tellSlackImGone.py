from machine import Pin
import urequests
import time

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("NETWORK NAME", "PASSWORD") # network name, network password
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def send_slack_alert(duration):
    url = 'https://hooks.slack.com/services/WEBHOOK_ID' # slack webhook url
    if duration == "long":
        payload = '{"text": "Brett will be away for over an hour"}'
    elif duration == "mid":
        payload = '{"text": "Brett will be away for up to an hour"}'
    elif duration == "back":
        payload = '{"text": "Brett is back"}'
    urequests.request("POST", url, data=payload)
    print("Button pressed")


do_connect()

btn_pressed = False
btnLong = Pin(0, Pin.IN, Pin.PULL_UP)
btnMid = Pin(4, Pin.IN, Pin.PULL_UP)
btnBack = Pin(5, Pin.IN, Pin.PULL_UP)
while True:
    if not btnLong.value() and not btn_pressed:
        btn_pressed = True
        dur = "long"
        send_slack_alert(dur)
        time.sleep(.2)
    elif not btnMid.value() and not btn_pressed:
        btn_pressed = True
        dur = "mid"
        send_slack_alert(dur)
        time.sleep(.2)
    elif not btnBack.value() and not btn_pressed:
        btn_pressed = True
        dur = "back"
        send_slack_alert(dur)
        time.sleep(.2)
    elif btnLong.value() and btnMid.value() and btnBack.value() and btn_pressed:
        btn_pressed = False
